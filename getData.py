from serpapi import GoogleSearch
import pandas as pd

params = {
    "api_key": "7160fd124ad77a622daf4eb617fd112c13dfb3fdda044fdfc25df24d27430e0c",  
    "engine": "google_maps",
    "q": "chinese restaurants Antananarivo",
    "ll": "@-18.8792,47.5079,15z",  
    "type": "search"
}

search = GoogleSearch(params)
results = search.get_dict()
restaurants = results.get("local_results", [])

# Stocker les données dans une liste
data = []
for restaurant in restaurants:
    data.append({
        "nom": restaurant.get("title", ""),
        "adresse": restaurant.get("address", ""),
        "type": restaurant.get("type", ""),
        "description": restaurant.get("description", ""),
        "link": restaurant.get("link", "")  # <--- récupère l'URL du site (souvent Facebook, TripAdvisor, etc.)
    })

# Sauvegarder dans un CSV
df = pd.DataFrame(data)
df.to_csv("restaurant", index=False)
print("restaurants_antananarivo_with_links.csv")
