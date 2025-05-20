import os
import shutil
import requests

# Créer dossier
os.makedirs("RESTAURANTS", exist_ok=True)
os.makedirs("RESTAURANTS/images", exist_ok=True)

# Télécharger image Le Jasmin
img_url = "https://www.facebook.com/photo/?fbid=912895374178628&set=a.488534023281434"
try:
    img_data = requests.get(img_url).content
    with open("RESTAURANTS/images/jasmin.jpg", "wb") as f:
        f.write(img_data)
except Exception as e:
    print(f"Échec téléchargement image Le Jasmin : {e}")

# Copier fichiers
files = [
    "restaurants_clean.csv", "restaurants_selected.csv", "restaurants_scored.csv",
    "graphe.png", "graphe_scores.gml", "rapport_authenticite.pdf"
]
for f in files:
    try:
        shutil.copy(f, "RESTAURANTS/")
    except FileNotFoundError:
        print(f"Fichier {f} manquant")

print("Archivage terminé : projet_restaurants/")
