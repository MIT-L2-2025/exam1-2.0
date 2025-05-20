import urllib.parse
import re
from apify_client import ApifyClient

# Clé API Apify
API_KEY = 'apify_api_CbOABx2d1zQJ0oju9nhPYQn2LpfEya4Dhx6T'


# Fonction pour vérifier les variables
def check_chinese_indicators(place):
    score = 0
    indicators = {"avis": False, "cuisine": False, "menu": False, "nom": False, "specialite": False}

    # Préparer les données avec gestion des None
    description = str(place.get("description", "")).lower()
    reviews = ""
    if isinstance(place.get("reviews"), list):
        reviews = " ".join([str(review.get("text", "")) for review in place.get("reviews", []) if isinstance(review.get("text", ""), str)]).lower()
    categories = " ".join([str(cat) for cat in place.get("categories", [])]).lower()
    menu_data = str(place.get("menu", place.get("menuItems", ""))).lower()

    # 1. Avis (30 % si positif et mentionne chinois)
    if re.search(r"(bonne|délicieux|excellente|savoureux|super|meilleur)\s*(chinois|chinese|cuisine chinoise)", description + reviews):
        indicators["avis"] = True
        score += 30
    if re.search(r"chinese|nems|riz cantonais|canard laqué|wonton|dim sum|porc caramélisé|cuisine chinoise", description + categories + reviews):
        indicators["cuisine"] = True
        score += 25

    # 3. Menu (20 % si plats chinois, -2 % par plat non chinois)
    chinese_dishes = r"nems|riz cantonais|canard laqué|dim sum|wonton|porc caramélisé|chop suey|porc aigre-doux"
    non_chinese_dishes = r"pizza|burger|pasta|steak|frites|sushi|tacos"
    if re.search(chinese_dishes, description + reviews + categories + menu_data):
        indicators["menu"] = True
        score += 20
    # Compter les plats non chinois
    non_chinese_matches = re.findall(non_chinese_dishes, description + reviews + categories + menu_data)
    score -= 2 * len(set(non_chinese_matches))  # -2 % par plat unique
    if score < 0:
        score = 0  # Éviter un score négatif

    # 4. Nom (25 %)
    name = str(place.get("title", "")).lower()
    if re.search(r"chine|dragon|muraille|lotus|jonquille|dynastie|orient", name):
        indicators["nom"] = True
        score += 25

    # 5. Spécialité (25 % si plat chinois)
    if re.search(chinese_dishes, description + categories):
        indicators["specialite"] = True
        score += 25

    # Lister les variables trouvées
    found_indicators = [key.capitalize() for key, value in indicators.items() if value]
    return score, indicators, found_indicators

# Fonction pour effectuer la recherche avec Apify
def search_restaurants():
    client = ApifyClient(API_KEY)
    antananarivo_coords = {'lat': -18.8792, 'lng': 47.5079}
    actor_id = 'compass~crawler-google-places'
    run_input = {
        'searchStringsArray': ['chinese restaurant'],
        'lat': antananarivo_coords['lat'],
        'lng': antananarivo_coords['lng'],
        'zoom': 12,
        'maxCrawledPlaces': 100,
        'language': 'fr',
        'includeGoogleReviews': True,
        'scrapePhoneNumbers': True,
        'includePhotos': True,
        'maxReviews': 5,
    }
    
    try:
        print(f"Lancement du scraping avec l'actor Apify : {actor_id}...")
        run = client.actor(actor_id).call(run_input=run_input)
        if run.get('defaultDatasetId'):
            dataset = client.dataset(run['defaultDatasetId']).list_items()
            results = dataset.items
            print(f"\nRestaurants trouvés ({len(results)}):")
            for place in results:
                print(f"- {place.get('title', 'Inconnu')} ({place.get('address', 'Non disponible')})")
            return results
        else:
            print("Aucun résultat trouvé dans le dataset.")
            return []
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return []

# Fonction pour filtrer les restaurants à Antananarivo
def is_in_antananarivo(place):
    address = place.get('address', '').lower()
    return 'antananarivo' in address or 'madagascar' in address

# Fonction pour générer le HTML
def generate_html(restaurants):
    html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurants Chinois à Antananarivo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }
        h1 { text-align: center; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #fff; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #b22222; color: white; }
        td { background-color: #fff; }
        img { max-width: 200px; height: auto; border-radius: 5px; }
        .probability { font-weight: bold; color: #2e8b57; }
        .variables { color: #555; }
        .maps-link { color: #0066cc; text-decoration: none; }
        .maps-link:hover { text-decoration: underline; }
        .footer { text-align: center; margin-top: 20px; font-size: 1.1em; color: #333; }
        .no-results { text-align: center; font-size: 1.2em; color: #e74c3c; }
        @media (max-width: 600px) {
            table, th, td { font-size: 14px; }
            img { max-width: 100px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Restaurants Chinois à Antananarivo</h1>
        <table>
            <thead>
                <tr>
                    <th>Photo</th>
                    <th>Nom</th>
                    <th>Adresse</th>
                    <th>Contact</th>
                    <th>Spécialité</th>
                    <th>Probabilité</th>
                    <th>Variables trouvées</th>
                    <th>Lien Google Maps</th>
                </tr>
            </thead>
            <tbody>
    """

    for restaurant in restaurants:
        html_content += f"""
                <tr>
                    <td><img src="{restaurant['photo']}" alt="{restaurant['name']}"></td>
                    <td>{restaurant['name']}</td>
                    <td>{restaurant['address']}</td>
                    <td>{restaurant['contact']}</td>
                    <td>{restaurant['specialty']}</td>
                    <td class="probability">{restaurant['probability']}%</td>
                    <td class="variables">{restaurant['variables']}</td>
                    <td><a href="{restaurant['maps_link']}" class="maps-link" target="_blank">Voir sur Google Maps</a></td>
                </tr>
        """

    html_content += f"""
            </tbody>
        </table>
        <div class="footer">
            Nombre total de restaurants chinois trouvés : {len(restaurants)}
        </div>
    </div>
</body>
</html>
    """

    with open("restaurants_chinois_antananarivo.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# Fonction principale
def main():
    data = search_restaurants()
    restaurants = []

    if data:
        print("\nRestaurants sélectionnés :")
        for place in data:
            if is_in_antananarivo(place):
                score, indicators, found_indicators = check_chinese_indicators(place)
                if score >= 10:
                    phone_keys = ['phoneNumber', 'phone', 'formattedPhoneNumber', 'contact']
                    phone = 'Non disponible'
                    for key in phone_keys:
                        if place.get(key):
                            phone = place.get(key)
                            break
                    thumbnail = place.get('thumbnailUrl', None)
                    photos = place.get('photos', [])
                    if photos and len(photos) > 0:
                        thumbnail = photos[0].get('url', None)
                    image_keys = ['image', 'imageUrl', 'mainImage']
                    for key in image_keys:
                        if place.get(key):
                            thumbnail = place.get(key)
                            break
                    photo = thumbnail if thumbnail else "https://via.placeholder.com/400x300?text=No+Image"
                    lat = place.get("location", {}).get("lat", 0)
                    lng = place.get("location", {}).get("lng", 0)
                    maps_link = f"https://www.google.com/maps?q={lat},{lng}" if lat and lng else "#"

                    restaurant = {
                        "name": place.get("title", "Inconnu"),
                        "address": place.get("address", "Non disponible"),
                        "contact": phone,
                        "lat": lat,
                        "lng": lng,
                        "specialty": "Cuisine chinoise (nems, riz cantonais, canard laqué)" if indicators["menu"] or indicators["cuisine"] else "Cuisine asiatique",
                        "photo": photo,
                        "probability": score,
                        "variables": ", ".join(found_indicators) if found_indicators else "Aucune",
                        "maps_link": maps_link
                    }
                    restaurants.append(restaurant)
                    print(f"- {restaurant['name']} ({restaurant['address']}) : {restaurant['variables']}")

    if not restaurants:
        print("Aucun restaurant chinois trouvé à Antananarivo.")
        return

    generate_html(restaurants)
    print(f"\nFichier HTML généré : restaurants_chinois_antananarivo.html")
    print(f"Nombre total de restaurants chinois trouvés : {len(restaurants)}")

if __name__ == "__main__":
    main()
