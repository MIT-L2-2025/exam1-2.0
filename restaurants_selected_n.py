import pandas as pd
import json

# Charger restaurants.json
with open("/home/manda/Téléchargements/MITL2/RESTAURANTS/restaurants.json") as f:
    data_json = json.load(f)
df = pd.DataFrame(data_json)

# Sélectionner restaurants avec noms suggérant cuisine asiatique
asian_keywords = ["chine", "jasmin", "saïgon", "dynastie"]
selected_restaurants = df[df["name"].str.contains("|".join(asian_keywords), case=False, na=False)]

# Si moins de n restaurants, prendre tous
n = len(df)  # Ou définir n (ex. : n = 5)
if len(selected_restaurants) < n:
    selected_restaurants = df.head(n)

# Ajouter colonnes manquantes
selected_restaurants["phone_number"] = "Non disponible"
selected_restaurants["rating"] = "N/A"
selected_restaurants["total_ratings"] = 0
selected_restaurants["menu"] = [
    "cochon de lait, tsa-siou" if "Le Grand Restaurant de Chine" in name else
    "magret de canard, teepan filet de zébu" if "Restaurants Le Jasmin-Analakely" in name else
    "fondue chinoise aux fruits de mer, dim sum" if "La Muraille de Chine" in name else
    "Croquettes de calmar,Steak au fromage " if "La Dynastie" in name else
    "pho, nems" if "Tanà Saïgon" in name else
    "pho, nems" if "Le Muguet " in name else
    "cuisine générique" for name in selected_restaurants["name"]
]
selected_restaurants["reviews"] = [
    "['à la vapeur', 'dim sum', 'saison des soupes']" if "Le Grand Restaurant de Chine" in name else
    "['Restos chinois d’un bon niveau', 'bonne cuisine', 'Très bonne cuisine chinoise']" if "Restaurants Le Jasmin-Analakely" in name else
    "['plats chinois cantonnais', 'Super dim sum', 'à la vapeur']" if "La Muraille de Chine" in name else
    "['saveurs asiatiques', 'cuisine fantasque', 'ambiance sympa']" if "La Dynastie" in name else
    "['authentique vietnamien', 'saveurs asiatiques', 'excellent']" if "Tanà Saïgon" in name else
    "['Snack', 'Grillade']" if "Le Muguet" in name else
    "['générique', 'correct']" for name in selected_restaurants["name"]
]
selected_restaurants["decor"] = [
    "Moderne, peu de décorations chinoises" if "Le Grand Restaurant de Chine" in name else
    "Lanternes rouges, dragon" if "Restaurants Le Jasmin-Analakely" in name else
    "Lanternes rouges, calligraphie" if "La Muraille de Chine" in name else
    "Ambiance asiatique, statues" if "La Dynastie" in name else
    "Décor vietnamien, bambou" if "Tanà Saïgon" in name else
    "moderne, meuble en bois" if "Le Muguet" in name else
    "Décor générique" for name in selected_restaurants["name"]
]

print(f"Sélectionné {len(selected_restaurants)} restaurants :")
print(selected_restaurants[["name", "address"]])
selected_restaurants.to_csv("/home/manda/Téléchargements/MITL2/RESTAURANTS/restaurants_selected_n.csv", index=False)
