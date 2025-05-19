import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from serpapi import GoogleSearch
import urllib

# Fonction pour vérifier les caractères chinois
def has_chinese_chars(text):
    if not text:
        return False
    return bool(re.search(r'[\u4e00-\u9fff]', text))

# Fonction pour scraper un site web
def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Type de cuisine
        is_chinese_cuisine = False
        cuisine_elements = soup.find_all(['span', 'div', 'p'], class_=re.compile('cuisine|category|type|specialty', re.I))
        for elem in cuisine_elements:
            if elem.text and ("chinese" in elem.text.lower() or "mandarin" in elem.text.lower() or "dim sum" in elem.text.lower()):
                is_chinese_cuisine = True
                break

        # Cuisine non chinoise
        has_non_chinese = False
        non_chinese_keywords = ["italian", "french", "indian", "lebanese", "mexican", "japanese", "thai"]
        for elem in cuisine_elements:
            if elem.text and any(keyword in elem.text.lower() for keyword in non_chinese_keywords):
                has_non_chinese = True
                break

        # Image du site
        image_url = None
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            image_url = og_image["content"]
        else:
            first_img = soup.find("img")
            if first_img and first_img.get("src"):
                image_url = first_img["src"]
                if image_url.startswith("//"):
                    image_url = "https:" + image_url
                elif image_url.startswith("/"):
                    image_url = urllib.parse.urljoin(url, image_url)

        return {
            "is_chinese_cuisine": is_chinese_cuisine,
            "has_non_chinese": has_non_chinese,
            "image_url": image_url
        }
    except Exception as e:
        print(f"Erreur lors du scraping de {url}: {e}")
        return {"is_chinese_cuisine": False, "has_non_chinese": False, "image_url": None}

# Fonction pour scraper les commentaires Google Maps
def scrape_comments(place_id, api_key):
    if not place_id:
        return False
    params = {
        "api_key": api_key,
        "engine": "google_maps_reviews",
        "place_id": place_id,
        "hl": "fr"
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        reviews = results.get("reviews", [])
        chinese_keywords = ["nems", "riz cantonais", "wok", "dim sum", "szechuan", "peking"]
        for review in reviews:
            text = review.get("snippet", "").lower()
            if any(keyword in text for keyword in chinese_keywords) or has_chinese_chars(text):
                return True
        return False
    except Exception as e:
        print(f"Erreur lors du scraping des avis pour place_id {place_id}: {e}")
        return False

# Charger le CSV
df = pd.read_csv("restaurants_antananarivo_with_place_ids.csv")

# Clé API
api_key = "f0e6bb4d0afbe2f2d22cea8afa975109bc22a9fde1612c54692859eee2751ad8"

# Initialisation des colonnes
df["score"] = 0
df["has_chinese_chars"] = df["nom"].apply(has_chinese_chars)
df["is_chinese_cuisine"] = False
df["has_chinese_comments"] = False
df["has_non_chinese"] = False
df["image_url"] = ""

# Boucle d’analyse
for index, row in df.iterrows():
    score = 0
    url = row["link"]
    place_id = row.get("place_id", "")

    # Scraping site web
    if isinstance(url, str) and url and "facebook.com" not in url:
        web_data = scrape_website(url)
        if web_data["is_chinese_cuisine"] or "chinese" in row["type"].lower():
            score += 5
            df.at[index, "is_chinese_cuisine"] = True
        if web_data["has_non_chinese"]:
            score -= 2
            df.at[index, "has_non_chinese"] = True
        if web_data["image_url"]:
            df.at[index, "image_url"] = web_data["image_url"]
    elif "chinese" in row["type"].lower() or "mandarin" in row["type"].lower() or "dim sum" in row["type"].lower():
        score += 5
        df.at[index, "is_chinese_cuisine"] = True

    # Nom avec caractères chinois
    if row["has_chinese_chars"]:
        score += 3

    # Commentaires Google
    if place_id:
        if scrape_comments(place_id, api_key):
            score += 2
            df.at[index, "has_chinese_comments"] = True

    # Score final
    score = max(0, min(10, score))
    df.at[index, "score"] = score

    time.sleep(2)

# Calcul du pourcentage
df["percentage_chinese"] = (df["score"] / 10) * 100

# Sauvegarde CSV
df.to_csv("restaurants_chinois_scored.csv", index=False)
print("Restaurants scorés sauvegardés dans restaurants_chinois_scored.csv")
print(df[["nom", "score", "percentage_chinese"]])

# Génération HTML
html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Restaurants Chinois à Antananarivo</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #333; margin-bottom: 20px; }
        .container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .card { background-color: #fff; border: 1px solid #ddd; border-radius: 8px; width: 300px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden; }
        .card img { width: 100%; height: 200px; object-fit: cover; }
        .card-content { padding: 15px; }
        .card-content h2 { margin: 0 0 10px; font-size: 1.2em; color: #d32f2f; }
        .card-content p { margin: 5px 0; color: #666; }
        .card-content .score { font-weight: bold; color: #2e7d32; }
        .card-content .percentage { font-weight: bold; color: #1976d2; }
        .btn { display: inline-block; padding: 8px 15px; background-color: #d32f2f; color: #fff; text-decoration: none; border-radius: 4px; margin-top: 10px; }
        .btn:hover { background-color: #b71c1c; }
    </style>
</head>
<body>
    <h1>Restaurants Chinois à Antananarivo</h1>
    <div class="container">
"""

for _, row in df.iterrows():
    encoded_address = urllib.parse.quote_plus(row['adresse'])
    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={encoded_address}"
    image_url = row.get("image_url", "https://via.placeholder.com/200x200?text=Pas+d'image")
    html_content += f"""
        <div class="card">
            <img src="{image_url}" alt="{row['nom']}">
            <div class="card-content">
                <h2>{row['nom']}</h2>
                <p><strong>Adresse:</strong> {row['adresse']}</p>
                <p><strong>Type:</strong> {row['type']}</p>
                <p><strong>Score:</strong> <span class="score">{row['score']}</span>/10</p>
                <p><strong>Probabilité Chinois:</strong> <span class="percentage">{row['percentage_chinese']:.1f}%</span></p>
                <a href="{maps_url}" target="_blank" class="btn">Voir l'itinéraire</a>
            </div>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

with open("restaurants_chinois_scored.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Page HTML générée : restaurants_chinois_scored.html")
