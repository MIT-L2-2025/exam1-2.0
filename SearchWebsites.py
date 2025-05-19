import pandas as pd
from serpapi import GoogleSearch
import time

# Charger le CSV
df = pd.read_csv("restaurants_antananarivo_with_links.csv")

# Clé API SerpApi
api_key = "f0e6bb4d0afbe2f2d22cea8afa975109bc22a9fde1612c54692859eee2751ad8"  # Ta clé

data = []
for index, row in df.iterrows():
    query = f"{row['nom']} Antananarivo"
    params = {
        "api_key": api_key,
        "engine": "google_maps",
        "q": query,
        "ll": "@-18.8792,47.5079,15z",
        "type": "search"
    }
    try:
        print(f"Recherche place_id pour : {row['nom']}")
        search = GoogleSearch(params)
        results = search.get_dict()
        place_id = results.get("local_results", [{}])[0].get("place_id", "")
        data.append({
            "nom": row["nom"],
            "adresse": row["adresse"],
            "type": row["type"],
            "description": row["description"],
            "link": row["link"],
            "place_id": place_id
        })
        time.sleep(2)
    except Exception as e:
        print(f"Erreur pour {row['nom']}: {e}")
        data.append({
            "nom": row["nom"],
            "adresse": row["adresse"],
            "type": row["type"],
            "description": row["description"],
            "link": row["link"],
            "place_id": ""
        })

# Sauvegarder
df_with_place_ids = pd.DataFrame(data)
df_with_place_ids.to_csv("restaurants_antananarivo_with_place_ids.csv", index=False)
print("CSV avec place_id généré : restaurants_antananarivo_with_place_ids.csv")