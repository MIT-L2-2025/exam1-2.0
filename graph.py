import networkx as nx
import tkinter as tk
import math
from typing import List, Dict, Tuple

# Données fictives pour le workflow avec scores hiérarchisés
workflow_data = [
    {"nom": "Restaurant Lotus", "latitude": -18.900, "longitude": 47.510, "classification": "Chinois", "score_total": 0.7},
    {"nom": "Restaurant Dragon", "latitude": -18.905, "longitude": 47.515, "classification": "Chinois", "score_total": 0.8},
    {"nom": "Restaurant Panda", "latitude": -18.910, "longitude": 47.520, "classification": "Chinois", "score_total": 0.9},
    {"nom": "Restaurant Jade", "latitude": -18.895, "longitude": 47.505, "classification": "Modérément Chinois", "score_total": 0.4},
    {"nom": "Restaurant Bamboo", "latitude": -18.900, "longitude": 47.500, "classification": "Modérément Chinois", "score_total": 0.5},
    {"nom": "Restaurant Orchid", "latitude": -18.905, "longitude": 47.495, "classification": "Modérément Chinois", "score_total": 0.6},
    {"nom": "Restaurant Soleil", "latitude": -18.915, "longitude": 47.525, "classification": "Non Chinois", "score_total": 0.1},
    {"nom": "Restaurant Étoile", "latitude": -18.920, "longitude": 47.530, "classification": "Non Chinois", "score_total": 0.2},
    {"nom": "Restaurant Lune", "latitude": -18.925, "longitude": 47.535, "classification": "Non Chinois", "score_total": 0.3}
]

# Fonction pour calculer la distance Haversine
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Fonction pour déterminer le poids d'une arête
def get_edge_weight(distance: float) -> float:
    if distance < 1:
        return 0.4
    elif distance < 5:
        return 0.2
    else:
        return 0.1

# Création du graphe pour le workflow
def create_workflow_graph(restaurants: List[Dict]) -> nx.Graph:
    G = nx.Graph()
    
    # Ajout des nœuds
    for restaurant in restaurants:
        G.add_node(
            restaurant["nom"],
            latitude=restaurant["latitude"],
            longitude=restaurant["longitude"],
            classification=restaurant["classification"],
            score_total=restaurant["score_total"]
        )
    
    # Ajout des arêtes (2 voisins les plus proches)
    for i, r1 in enumerate(restaurants):
        distances = []
        for j, r2 in enumerate(restaurants):
            if i != j:
                distance = haversine_distance(
                    r1["latitude"], r1["longitude"],
                    r2["latitude"], r2["longitude"]
                )
                distances.append((r2["nom"], distance))
        distances.sort(key=lambda x: x[1])
        for neighbor, distance in distances[:min(2, len(distances))]:
            weight = get_edge_weight(distance)
            G.add_edge(r1["nom"], neighbor, weight=weight, distance=distance)
    
    return G

# Application Tkinter pour la visualisation
class WorkflowGraphApp:
    def __init__(self, root, G):
        self.G = G
        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack(pady=20)
        
        # Couleurs des nœuds
        self.color_map = {
            "Chinois": "red",
            "Modérément Chinois": "blue",
            "Non Chinois": "green"
        }
        
        # Initialiser les positions des nœuds (disposition de force)
        self.node_positions = {}
        self.node_items = {}
        self.node_labels = {}
        self.node_selected = None
        
        # Disposition de force
        spring_pos = nx.spring_layout(G, k=0.7, iterations=50)
        canvas_width = 500
        canvas_height = 400
        margin = 50
        
        for node in G.nodes:
            x, y = spring_pos[node]
            x = margin + (x + 1) / 2 * (canvas_width - 2 * margin)
            y = margin + (1 - y) / 2 * (canvas_height - 2 * margin)
            self.node_positions[node] = [x, y]
        
        # Dessiner le graphe
        self.draw_graph()
        
        # Lier les événements
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Motion>", self.show_tooltip)
        
        # Ajouter légende et bouton de sauvegarde
        self.add_legend()
        tk.Button(root, text="Sauvegarder le graphe", command=self.save_graph).pack()
    
    def draw_graph(self):
        self.canvas.delete("all")
        
        # Grille légère
        for x in range(50, 550, 50):
            self.canvas.create_line(x, 50, x, 450, fill="#e0e0e0", dash=(2, 2))
        for y in range(50, 450, 50):
            self.canvas.create_line(50, y, 550, y, fill="#e0e0e0", dash=(2, 2))
        
        # Dessiner les arêtes
        for u, v in self.G.edges:
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            weight = self.G[u][v]["weight"]
            distance = self.G[u][v]["distance"]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=weight * 10)
            self.canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2,
                text=f"{distance:.2f} km\nPoids: {weight}",
                fill="black", font=("Arial", 8)
            )
        
        # Dessiner les nœuds
        for node in G.nodes:
            x, y = self.node_positions[node]
            size = self.G.nodes[node]["score_total"] * 30 + 10
            color = self.color_map.get(self.G.nodes[node]["classification"], "gray")
            self.node_items[node] = self.canvas.create_oval(
                x - size, y - size, x + size, y + size, fill=color, outline="black", width=2
            )
            self.node_labels[node] = self.canvas.create_text(
                x, y - size - 10, text=node, font=("Arial", 10, "bold"), fill="black"
            )
    
    def start_drag(self, event):
        x, y = event.x, event.y
        min_dist = float("inf")
        for node in self.G.nodes:
            nx, ny = self.node_positions[node]
            dist = math.sqrt((x - nx) ** 2 + (y - ny) ** 2)
            if dist < min_dist and dist < 20:
                min_dist = dist
                self.node_selected = node
        self.last_x = x
        self.last_y = y
    
    def drag(self, event):
        if self.node_selected:
            x, y = event.x, event.y
            self.node_positions[self.node_selected] = [x, y]
            self.draw_graph()
            self.last_x = x
            self.last_y = y
    
    def stop_drag(self, event):
        self.node_selected = None
    
    def show_tooltip(self, event):
        self.canvas.delete("tooltip")
        x, y = event.x, event.y
        for node in self.G.nodes:
            nx, ny = self.node_positions[node]
            if math.sqrt((x - nx) ** 2 + (y - ny) ** 2) < 20:
                tooltip_text = f"{node}\nScore: {self.G.nodes[node]['score_total']}\nClass: {self.G.nodes[node]['classification']}"
                self.canvas.create_text(x + 20, y, text=tooltip_text, tags="tooltip", anchor="w", font=("Arial", 8))
                break
    
    def add_legend(self):
        legend_x, legend_y = 500, 50
        for i, (cls, color) in enumerate(self.color_map.items()):
            self.canvas.create_oval(legend_x - 10, legend_y + i * 30 - 10, legend_x + 10, legend_y + i * 30 + 10, fill=color)
            self.canvas.create_text(legend_x + 20, legend_y + i * 30, text=cls, anchor="w", font=("Arial", 10))
    
    def save_graph(self):
        self.canvas.postscript(file="workflow_fictif_graph.ps", colormode="color")
        print("Graphe sauvegardé sous workflow_fictif_graph.ps")

# Exécution principale
if __name__ == "__main__":
    restaurants = workflow_data
    if restaurants:
        G = create_workflow_graph(restaurants)
        root = tk.Tk()
        root.title("🌟 Graphe du Workflow Fictif des Restaurants 🌟")
        app = WorkflowGraphApp(root, G)
        root.mainloop()
    else:
        print("Aucune donnée à visualiser.")
