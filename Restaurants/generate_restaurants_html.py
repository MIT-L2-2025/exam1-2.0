import json
import os
import urllib.parse
from scipy.stats import chisquare

GOOGLE_MAPS_API_KEY = "AIzaSyD26SBDx0y_zVHM30FGrC0BiQm6RrJwpmM"

# Liste de mots-clés associés à la cuisine chinoise
CHINESE_KEYWORDS = [
    "riz cantonais", "nouilles", "wonton", "dim sum", "canard laqué", "szechuan",
    "tofu", "porc aigre-doux", "nems", "raviolis", "soja", "sésame", "soupe asiatique",
    "bœuf sauté", "poulet impérial", "crevettes sauce piquante", "chinois", "chinese",
    "mandarin", "sichuan", "cantonnais"
]

# Charger les données JSON
with open('/app/Téléchargements/file.json', 'r', encoding='utf-8') as file:
    restaurants = json.load(file)

def calculate_authenticity_score(restaurant):
    """Calcule le score d'authenticité chinoise (0-100%) basé sur les données JSON."""
    category = restaurant.get('categoryName', '').lower()
    if 'chinese restaurant' in category or 'mandarin restaurant' in category:
        category_score = 100
    elif 'hot pot restaurant' in category or 'asian fusion restaurant' in category:
        category_score = 80
    elif 'asian restaurant' in category or 'pan-asian restaurant' in category:
        category_score = 60
    else:
        category_score = 20

    title = restaurant.get('title', '').lower()
    keyword_hits = sum(1 for kw in CHINESE_KEYWORDS if kw.lower() in title)
    keyword_score = min(100, keyword_hits * 20)

    offerings = restaurant.get('additionalInfo', {}).get('Offerings', [])
    offering_tags = [key for offering in offerings for key, value in offering.items() if value]
    offering_keywords = ['small plates', 'organic dishes', 'vegan options', 'vegetarian options']
    offering_hits = sum(1 for tag in offering_tags if tag.lower() in offering_keywords)
    offering_score = min(100, offering_hits * 25)

    total_score = restaurant.get('totalScore', 0)
    rating_score = (total_score / 5.0) * 100 if total_score else 0

    authenticity_score = (
        0.4 * category_score +
        0.3 * keyword_score +
        0.2 * offering_score +
        0.1 * rating_score
    )
    return round(authenticity_score, 2)

def calculate_chi_square_score(restaurant):
    """Calcule un score khi-deux basé sur les mots-clés dans le nom du restaurant."""
    title = restaurant.get('title', '').lower()
    total_keywords = len(CHINESE_KEYWORDS)
    observed_keywords = sum(1 for kw in CHINESE_KEYWORDS if kw.lower() in title)
    observed_non_keywords = total_keywords - observed_keywords
    expected_keywords = total_keywords * 0.1
    expected_non_keywords = total_keywords - expected_keywords
    
    observed = [observed_keywords, observed_non_keywords]
    expected = [expected_keywords, expected_non_keywords]
    
    if expected_keywords == 0 or expected_non_keywords == 0:
        return 0.0
    
    chi_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
    chi_score = round((1 - p_value) * 100, 2)
    return max(0, min(100, chi_score))

def format_opening_hours(hours):
    if not hours:
        return "Non disponible"
    formatted = ""
    for entry in hours:
        day = entry.get('day', 'Inconnu')
        hours_str = entry.get('hours', 'Non disponible')
        formatted += f"{day}: {hours_str}<br>"
    return formatted

def generate_street_view_url(lat, lng, api_key):
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "640x400",
        "location": f"{lat},{lng}",
        "heading": "0",
        "pitch": "0",
        "fov": "80",
        "key": api_key
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def normalize_coordinates(restaurant):
    """Normalise les coordonnées d'un restaurant pour l'espace 3D."""
    lat = restaurant.get('latitude', None)
    lng = restaurant.get('longitude', None)
    authenticity_score = restaurant.get('authenticity_score', 0)
    
    center_lat = -18.8792
    center_lng = 47.5079
    
    norm_lat = 0
    norm_lng = 0
    if lat is not None and lng is not None:
        norm_lat = (lat - center_lat) * 50
        norm_lng = (lng - center_lng) * 50
        norm_lat = max(-5, min(5, norm_lat))
        norm_lng = max(-5, min(5, norm_lng))
    
    return {
        'norm_lat': norm_lat,
        'norm_lng': norm_lng,
        'authenticity_score': authenticity_score
    }

# Ajouter les scores
for restaurant in restaurants:
    restaurant['authenticity_score'] = calculate_authenticity_score(restaurant)
    restaurant['chi_square_score'] = calculate_chi_square_score(restaurant)

# Trier les restaurants
restaurants.sort(key=lambda x: x['authenticity_score'], reverse=True)

# Génération HTML
html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurants Chinois à Antananarivo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Roboto', sans-serif; background-color: #f8f9fa; }
        .navbar { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .restaurant-card { transition: transform 0.2s; }
        .restaurant-card:hover { transform: translateY(-5px); }
        .restaurant-canvas { width: 300px; height: 150px; border: 1px solid #dee2e6; border-radius: 8px; background: #fff; }
        .tooltip-inner { background-color: #343a40; color: white; }
        .error-message { margin: 10px 0; }
        .canvas-container { display: none; }
        .canvas-container.active { display: block; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#">Restaurants Chinois</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#top">Haut de page</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5 pt-5">
        <h1 class="text-center mb-4">Restaurants Chinois à Antananarivo</h1>
        <div class="row">
"""

for idx, restaurant in enumerate(restaurants):
    title = restaurant.get('title', 'Nom inconnu')
    address = restaurant.get('address', 'Adresse inconnue')
    phone = restaurant.get('phone', 'Non disponible')
    opening_hours = restaurant.get('openingHours', [])
    image_url = restaurant.get('imageUrl', '')
    maps_url = restaurant.get('url', '#')
    category = restaurant.get('categoryName', 'Non spécifié')
    score = restaurant.get('totalScore', 'N/A')
    lat = restaurant.get('latitude')
    lng = restaurant.get('longitude')
    authenticity_score = restaurant.get('authenticity_score', 0)
    chi_square_score = restaurant.get('chi_square_score', 0)

    street_img = generate_street_view_url(lat, lng, GOOGLE_MAPS_API_KEY) if lat and lng else ""
    hours = format_opening_hours(opening_hours)
    viz_data = normalize_coordinates(restaurant)
    has_coords = lat is not None and lng is not None

    # Badge pour le score d'authenticité
    badge_class = "bg-success" if authenticity_score >= 70 else "bg-warning" if authenticity_score >= 40 else "bg-danger"

    html_content += f"""
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card restaurant-card h-100 shadow-sm">
                    <div class="card-body">
                        <h3 class="card-title">{title}</h3>
                        <p>
                            <strong>Authenticité :</strong>
                            <span class="badge {badge_class}" data-bs-toggle="tooltip" data-bs-placement="top" title="Score basé sur catégorie, nom, tags et note Google">{authenticity_score}%</span>
                        </p>
                        <p>
                            <strong>Score khi-deux :</strong>
                            <span class="badge bg-info" data-bs-toggle="tooltip" data-bs-placement="top" title="Significativité des mots-clés chinois dans le nom">{chi_square_score}%</span>
                        </p>
    """
    
    if has_coords:
        html_content += f"""
                        <p>Visualisation 3D : Sphère positionnée selon longitude (X), latitude (Y), score d'authenticité (Z). Couleur basée sur le score khi-deux.</p>
                        <button class="btn btn-outline-primary btn-sm mb-2" onclick="toggleCanvas('canvas-container-{idx}')">Afficher la visualisation 3D</button>
                        <div id="canvas-container-{idx}" class="canvas-container">
                            <canvas id="canvas-restaurant-{idx}" class="restaurant-canvas" aria-label="Visualisation 3D du restaurant {title}"></canvas>
                        </div>
                        <script>
                            function initCanvas{idx}() {{
                                const restaurant = {{
                                    title: {json.dumps(title)},
                                    norm_lat: {viz_data['norm_lat']},
                                    norm_lng: {viz_data['norm_lng']},
                                    authenticity_score: {viz_data['authenticity_score']},
                                    chi_square_score: {chi_square_score}
                                }};
                                
                                const scene = new THREE.Scene();
                                const canvas = document.getElementById('canvas-restaurant-{idx}');
                                const renderer = new THREE.WebGLRenderer({{ canvas: canvas }});
                                renderer.setSize(300, 150);
                                
                                const camera = new THREE.PerspectiveCamera(75, 300 / 150, 0.1, 1000);
                                camera.position.set(0, 5, 5);
                                camera.lookAt(0, 0, 0);
                                
                                const controls = new THREE.OrbitControls(camera, renderer.domElement);
                                controls.enableDamping = true;
                                controls.dampingFactor = 0.05;
                                
                                const light = new THREE.AmbientLight(0xffffff, 0.8);
                                scene.add(light);
                                
                                const geometry = new THREE.SphereGeometry(0.3, 32, 32);
                                const hue = restaurant.chi_square_score / 300;
                                const color = new THREE.Color().setHSL(hue, 1, 0.5);
                                const material = new THREE.MeshPhongMaterial({{ color: color }});
                                const sphere = new THREE.Mesh(geometry, material);
                                sphere.position.set(
                                    restaurant.norm_lng,
                                    restaurant.norm_lat,
                                    restaurant.authenticity_score / 10
                                );
                                sphere.userData = {{
                                    title: restaurant.title,
                                    authenticity: restaurant.authenticity_score
                                }};
                                scene.add(sphere);
                                
                                const raycaster = new THREE.Raycaster();
                                const mouse = new THREE.Vector2();
                                let tooltip = document.createElement('div');
                                tooltip.className = 'tooltip';
                                document.body.appendChild(tooltip);
                                
                                canvas.addEventListener('mousemove', (event) => {{
                                    const rect = canvas.getBoundingClientRect();
                                    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                                    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
                                    
                                    raycaster.setFromCamera(mouse, camera);
                                    const intersects = raycaster.intersectObjects(scene.children.filter(obj => obj.isMesh));
                                    
                                    if (intersects.length > 0) {{
                                        const data = intersects[0].object.userData;
                                        tooltip.style.left = event.clientX + 10 + 'px';
                                        tooltip.style.top = event.clientY + 10 + 'px';
                                        tooltip.innerHTML = `${{data.title}}<br>Authenticité: ${{data.authenticity}}%`;
                                        tooltip.style.display = 'block';
                                    }} else {{
                                        tooltip.style.display = 'none';
                                    }}
                                }});
                                
                                function animate() {{
                                    requestAnimationFrame(animate);
                                    controls.update();
                                    renderer.render(scene, camera);
                                }}
                                animate();
                            }}
                        </script>
        """
    else:
        html_content += """
                        <div class="alert alert-warning error-message" role="alert">
                            Visualisation 3D non disponible : Coordonnées manquantes.
                        </div>
        """

    html_content += f"""
                        {f'<img src="{street_img}" class="card-img-top mt-2" alt="Street View de {title}" style="border-radius: 8px;">' if street_img else ''}
                        {f'<img src="{image_url}" class="card-img-top mt-2" alt="Photo de {title}" style="border-radius: 8px;">' if image_url else ''}
                        <p class="mt-2"><strong>Catégorie :</strong> {category}</p>
                        <p><strong>Adresse :</strong> {address}</p>
                        <p><strong>Téléphone :</strong> {phone}</p>
                        <p><strong>Note Google :</strong> {score}/5</p>
                        <p><strong>Horaires :</strong><br>{hours}</p>
                        <a href="{maps_url}" class="btn btn-primary btn-sm" target="_blank">Voir sur Google Maps</a>
                    </div>
                </div>
            </div>
    """

html_content += """
        </div>
    </div>
    <footer class="bg-light text-center py-3 mt-4">
        <p class="mb-0">Généré le 20 mai 2025</p>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        // Initialiser les tooltips Bootstrap
        document.addEventListener('DOMContentLoaded', () => {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.forEach(tooltipTriggerEl => {
                new bootstrap.Tooltip(tooltipTriggerEl);
            });
        });
        
        // Fonction pour basculer l'affichage du canvas
        function toggleCanvas(containerId) {
            const container = document.getElementById(containerId);
            if (!container.classList.contains('active')) {
                container.classList.add('active');
                // Initialiser le canvas uniquement au premier affichage
                if (!container.dataset.initialized) {
                    window['initCanvas' + containerId.split('-')[2]]();
                    container.dataset.initialized = 'true';
                }
            } else {
                container.classList.remove('active');
            }
        }
    </script>
</body>
</html>
"""

with open('/app/Téléchargements/restaurants_chinois.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML généré avec restaurants triés par authenticité chinoise, visualisation 3D individuelle et affichage amélioré.")
