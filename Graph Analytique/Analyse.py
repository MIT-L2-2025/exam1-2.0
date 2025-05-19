import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from collections import defaultdict


class ChineseRestaurantAnalyzer:
    """Class for analyzing Chinese restaurants from data and visualizing results."""
    
    def __init__(self, file_path='rest_sample.json'):
        """Initialize the analyzer with data from a JSON file."""
        self.restaurants = self._load_data(file_path)
        self.neighborhoods = [
            {'name': 'Behoririka', 'lat': -18.9000, 'lon': 47.5200, 'score': 0.6},
            {'name': 'Analakely', 'lat': -18.9100, 'lon': 47.5250, 'score': 0.5},
            {'name': 'Andrahavoangy', 'lat': -18.8900, 'lon': 47.5100, 'score': 0.5},
            {'name': 'Ankorondrano', 'lat': -18.8700, 'lon': 47.5300, 'score': 0.5},
            {'name': 'Ivato', 'lat': -18.8000, 'lon': 47.4800, 'score': 0.6}
        ]
        self.chinese_names = set(['li', 'chen', 'wang', 'zhang', 'liu', 'yang', 'huang', 'zhao', 'wu', 'zhou', 'xu', 'sun', 'ma', 'zhu', 'hu', 'guo', 'lin', 'he', 'gao', 'luo', 'ying'])
        
        # Positive and negative keywords for different categories
        self.keywords = {
            'name': {
                'positive': ['chinois', 'china', 'qing', 'dragon', 'panda', 'jasmine', 'wan', 'lotus', 'jade', 'shi fu', 
                           'hao', 'rouge', 'empire', 'dynasty', 'tsang', 'chinese', 'hong kong', 'fleur', 'orient', 
                           'oriental', 'beijing', 'shanghai', 'peking', 'wok', 'xin', 'fu', 'jin', 'yu', 'ming'],
                'negative': ['malagasy', 'gargotte', 'sushi', 'thai', 'vietnam', 'pizza', 'burger', 'indian']
            },
            'text': {
                'positive': ['yum cha', 'dim sum', 'canard laqué', 'mapo tofu', 'xiaolongbao', 'authentique chinois',
                           'cuisine sichuanaise', 'cuisine cantonaise', 'wonton', 'raviolis chinois', '飲茶', 
                           'authentique', 'authentic', 'tofu', 'noodle', 'noodles', 'chinois', 'chinese', 'cantonais', 
                           'the', 'pao', 'tea', 'nouilles', 'cantonese', 'cantonese rice', 'dumplings', 'baozi', 
                           'jiaozi', 'chow mein', 'spring roll'],
                'negative': ['malagasy', 'vazaha', 'ravitoto', 'sushi', 'pad thai', 'pizza', 'burger', 'curry']
            }
        }
    
    def _load_data(self, file_path):
        """Load restaurant data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data[0]['restaurants']
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return []
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing JSON data: {e}")
            return []
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate the Haversine distance between two points in kilometers."""
        R = 6371  # Earth's radius in km
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    
    def name_chineseness(self, name):
        """Calculate how Chinese a restaurant name appears to be."""
        if not name:
            return 0
            
        score = 0
        # Check for Chinese characters
        if re.search(r'[\u4e00-\u9fff]', name):
            score += 0.7
            
        name_lower = name.lower()
        # Check for positive keywords
        for keyword in self.keywords['name']['positive']:
            if keyword.lower() in name_lower:
                score += 0.3
                break
                
        # Check for negative keywords
        for keyword in self.keywords['name']['negative']:
            if keyword.lower() in name_lower:
                score -= 0.3
                break
                
        return max(0, min(1, score))
    
    def location_chineseness(self, lat, lon, vicinity):
        """Calculate how likely a location is to be in a Chinese neighborhood."""
        if not lat or not lon:
            return 0.1
            
        vicinity = vicinity.lower() if vicinity else ""
        score = 0.1  # Default score
        
        # Check proximity to known Chinese neighborhoods
        proximity_radius = 2  # km
        for neighborhood in self.neighborhoods:
            distance = self.haversine_distance(lat, lon, neighborhood['lat'], neighborhood['lon'])
            if distance <= proximity_radius:
                score = neighborhood['score']
                break
            if neighborhood['name'].lower() in vicinity:
                score = neighborhood['score']
                break
                
        return score
    
    def authors_chineseness(self, authors):
        """Calculate how likely review authors are to be Chinese."""
        if not authors or authors.strip() == 'Unknown':
            return 0
            
        authors_lower = authors.lower()
        score = 0
        
        # Check for Chinese names
        for name in self.chinese_names:
            if f" {name} " in f" {authors_lower} " or f"{name}," in authors_lower:
                score += 0.5
                break
                
        # Check for Chinese characters
        if re.search(r'[\u4e00-\u9fff]', authors_lower):
            score += 0.7
            
        return min(score, 1)
    
    def text_chineseness(self, text):
        """Calculate how Chinese-related the review text appears to be."""
        if not text or text.strip() == '':
            return 0
            
        text_lower = text.lower()
        score = 0
        
        # Check for Chinese characters
        if re.search(r'[\u4e00-\u9fff]', text_lower):
            score += 0.6
        
        # Check for positive keywords
        for keyword in self.keywords['text']['positive']:
            if keyword.lower() in text_lower:
                score += 0.4
                break
                
        # Check for negative keywords
        for keyword in self.keywords['text']['negative']:
            if keyword.lower() in text_lower:
                score -= 0.3
                break
                
        return max(0, min(1, score))
    
    def rating_chineseness(self, rating):
        """Calculate how likely a rating is to indicate an authentic Chinese restaurant."""
        if not rating or rating.strip() == '':
            return 0
            
        try:
            # Extract numbers from rating string
            ratings = [float(r) for r in re.findall(r'\d+(?:\.\d+)?', rating)]
            if not ratings:
                return 0
                
            avg_rating = sum(ratings) / len(ratings)
            
            # Higher ratings get higher scores
            if avg_rating >= 4.5:
                return 0.8
            elif avg_rating >= 4:
                return 0.6
            elif avg_rating >= 3.5:
                return 0.4
            elif avg_rating >= 3:
                return 0.2
            else:
                return 0.1
        except ValueError:
            return 0
    
    def create_bipartite_graph(self):
        """Create a bipartite graph connecting restaurants to Chinese attributes."""
        G = nx.Graph()
        
        # Define node sets
        X = [r['name'] for r in self.restaurants]
        Y = ['Chinese Name', 'Chinese Location', 'Chinese Reviewers', 'Authentic Reviews', 'High Rating']
        
        # Add nodes
        G.add_nodes_from(X, bipartite=0)  # Restaurants
        G.add_nodes_from(Y, bipartite=1)  # Attributes
        
        # Calculate scores and add edges
        for restaurant in self.restaurants:
            r_name = restaurant['name']
            scores = [
                self.name_chineseness(restaurant['name']),
                self.location_chineseness(
                    restaurant.get('latitude', 0), 
                    restaurant.get('longitude', 0), 
                    restaurant.get('vicinity', '')
                ),
                self.authors_chineseness(restaurant.get('all_authors', '')),
                self.text_chineseness(restaurant.get('all_text', '')),
                self.rating_chineseness(restaurant.get('all_rating', ''))
            ]
            
            # Add edges with weight >= threshold
            for j, score in enumerate(scores):
                threshold = 0.15  # Slightly higher threshold to reduce noise
                if score >= threshold:
                    G.add_edge(r_name, Y[j], weight=score)
        
        return G, X, Y
    
    def shorten_name(self, name, max_length=20):
        """Shorten long names for better visualization."""
        return (name[:max_length] + '...') if len(name) > max_length else name
    
    def setup_dark_theme(self):
        """Set up dark theme for plots."""
        plt.style.use('dark_background')
        
        # Custom dark theme colors
        self.colors = {
            'background': '#1E1E1E',
            'text': '#E0E0E0',
            'grid': '#333333',
            'restaurants': '#FF5F5F',  # Red-tinted
            'attributes': '#5FB8FF',    # Blue-tinted
            'edge_cmap': plt.cm.inferno,
            'edge_color': '#FFAA00',
            'label_color': '#E0E0E0'
        }
    
    def visualize_graph(self, G, X, Y, show_weights=True, edge_threshold=0.3, save_path='chinese_restaurant_graph_dark.png'):
        """Create a visually appealing dark-themed graph visualization."""
        self.setup_dark_theme()
        
        # Figure setup with dark background
        fig, ax = plt.subplots(figsize=(16, 12), facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])
        
        # Prepare node positions - improved layout
        pos = nx.bipartite_layout(G, X, scale=2.0)
        
        # Adjust positions to spread nodes better
        for node in X:
            pos[node][1] += np.random.uniform(-0.1, 0.1)
        
        # Draw nodes with enhanced styling
        restaurants_nodes = nx.draw_networkx_nodes(
            G, pos, nodelist=X, 
            node_color=self.colors['restaurants'],
            node_shape='o', 
            node_size=800,
            edgecolors='#FF8080',
            linewidths=1.5,
            alpha=0.85,
            label='Restaurants'
        )
        
        # Add drop shadow effect
        restaurants_nodes.set_zorder(2)
        
        attributes_nodes = nx.draw_networkx_nodes(
            G, pos, nodelist=Y, 
            node_color=self.colors['attributes'],
            node_shape='h',  # Hexagon shape for attributes
            node_size=1200,
            edgecolors='#80C0FF',
            linewidths=1.5,
            alpha=0.9,
            label='Chinese Attributes'
        )
        attributes_nodes.set_zorder(3)
        
        # Draw edges with color gradient based on weight
        edges = G.edges(data=True)
        weights = [d['weight'] for u, v, d in edges]
        
        nx.draw_networkx_edges(
            G, pos, 
            edge_color=weights,
            edge_cmap=self.colors['edge_cmap'],
            width=[w*3 for w in weights],  # Width proportional to weight
            alpha=0.7,
            edge_vmin=0.15,
            edge_vmax=1
        )
        
        # Draw edge labels for significant connections
        if show_weights:
            edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in edges if d['weight'] >= edge_threshold}
            nx.draw_networkx_edge_labels(
                G, pos, 
                edge_labels=edge_labels,
                font_size=9,
                font_color='#FFDD99',
                font_family='monospace',
                font_weight='bold',
                bbox=dict(facecolor=self.colors['background'], edgecolor='none', alpha=0.7, pad=0.3),
                label_pos=0.6
            )
        
        # Draw node labels with better formatting
        rest_labels = {node: self.shorten_name(node) for node in X}
        attr_labels = {node: node for node in Y}
        
        # Restaurant labels
        nx.draw_networkx_labels(
            G, pos,
            labels=rest_labels,
            font_size=10,
            font_weight='bold',
            font_color='#FFE0E0',
            font_family='sans-serif',
            verticalalignment='center'
        )
        
        # Attribute labels
        nx.draw_networkx_labels(
            G, pos,
            labels=attr_labels,
            font_size=11,
            font_weight='bold',
            font_color='#E0F0FF',
            font_family='sans-serif',
            verticalalignment='center'
        )
        
        # Add legend and title
        plt.legend(
            [restaurants_nodes, attributes_nodes],
            ['Restaurants', 'Chinese Attributes'],
            loc='upper right',
            facecolor=self.colors['background'],
            edgecolor='#555555',
            labelcolor=self.colors['text'],
            fontsize=12
        )
        
        plt.title(
            'Chinese Restaurant Classification Network',
            fontsize=16,
            color=self.colors['text'],
            fontweight='bold',
            pad=20
        )
        
        # Add colorbar for edge weights
        sm = plt.cm.ScalarMappable(cmap=self.colors['edge_cmap'], norm=plt.Normalize(0.15, 1))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label('Chinese Attribute Score', color=self.colors['text'], fontsize=12)
        cbar.ax.tick_params(colors=self.colors['text'])
        
        # Add info text
        plt.figtext(
            0.01, 0.01,
            'Edge thickness and color indicate strength of Chinese characteristics',
            color=self.colors['text'],
            fontsize=10
        )
        
        # Remove axis
        plt.axis('off')
        
        # Create tight layout and save with high resolution
        plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=self.colors['background'])
        plt.show()
        
    def analyze_most_authentic(self, G, top_n=5):
        """Analyze and return the most authentically Chinese restaurants."""
        # Calculate a weighted authenticity score for each restaurant
        restaurant_scores = defaultdict(float)
        
        for restaurant in self.restaurants:
            name = restaurant['name']
            # Calculate each attribute score
            scores = {
                'name': self.name_chineseness(restaurant['name']),
                'location': self.location_chineseness(
                    restaurant.get('latitude', 0), 
                    restaurant.get('longitude', 0), 
                    restaurant.get('vicinity', '')
                ),
                'authors': self.authors_chineseness(restaurant.get('all_authors', '')),
                'text': self.text_chineseness(restaurant.get('all_text', '')),
                'rating': self.rating_chineseness(restaurant.get('all_rating', ''))
            }
            
            # Weighted average (give more weight to text and name)
            weights = {'name': 0.3, 'location': 0.15, 'authors': 0.15, 'text': 0.25, 'rating': 0.15}
            weighted_score = sum(scores[k] * weights[k] for k in scores)
            restaurant_scores[name] = weighted_score
        
        # Sort restaurants by score
        sorted_restaurants = sorted(restaurant_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_restaurants[:top_n]
        
    def run_analysis(self, save_path='chinese_restaurant_graph_dark.png'):
        """Run the full analysis and visualization pipeline."""
        if not self.restaurants:
            print("No restaurant data available. Analysis aborted.")
            return
            
        # Create bipartite graph
        G, X, Y = self.create_bipartite_graph()
        
        # Visualize graph
        self.visualize_graph(G, X, Y, save_path=save_path)
        
        # Print analysis of most authentic Chinese restaurants
        most_authentic = self.analyze_most_authentic(G)
        print("\n=== Most Authentically Chinese Restaurants ===")
        for i, (name, score) in enumerate(most_authentic, 1):
            print(f"{i}. {name}: {score:.3f}")
        
        # Print network statistics
        print("\n=== Network Statistics ===")
        print(f"Number of restaurants: {len(X)}")
        print(f"Total edges: {G.number_of_edges()}")
        print(f"Network density: {nx.density(G):.3f}")
        
        # Print nodes with highest degree
        degrees = dict(G.degree())
        top_connected = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
        print("\n=== Most Connected Nodes ===")
        for node, degree in top_connected:
            print(f"{node}: connected to {degree} nodes")


# Run the analysis
if __name__ == "__main__":
    analyzer = ChineseRestaurantAnalyzer('rest_sample.json')
    analyzer.run_analysis()
