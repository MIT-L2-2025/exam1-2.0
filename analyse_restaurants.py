import pandas as pd
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import re
import shutil
import os

# Étape 1 : Calculer scores
try:
    df = pd.read_csv("/home/manda/Téléchargements/MITL2/RESTAURANTS/restaurants_selected_n.csv")
    print(f"Chargé {len(df)} restaurants depuis restaurants_selected_n.csv")
except FileNotFoundError:
    print("Erreur : restaurants_selected_n.csv manquant. Exécutez create_restaurants_selected_n.py ou restaurants_selected.py.")
    exit()

nlp = spacy.load("fr_core_news_sm")
keywords = [
    "authentique", "chinois", "dim sum", "tsa-siou", "kung pao", "sichuan",
    "cantonnais", "lanternes", "calligraphie", "dragon", "aigre-doux",
    "chow mein", "nems", "cuisine chinoise", "vapeur", "soupes",
    "bibimbap", "kimchi", "coréen", "asiatique", "indienne", "teepan",
    "pho", "vietnamien"
]

def score_authenticity(texts):
    if not texts or texts == "":
        return 0
    score = 0
    texts = eval(texts) if isinstance(texts, str) and texts.startswith("[") else [texts]
    for text in texts:
        text = str(text).lower()
        doc = nlp(text)
        score += sum(1 for token in doc if token.text in keywords)
        score += sum(1 for kw in keywords if kw in text and kw not in [token.text for token in doc])
    return min(score, 5)

# Calculer scores bruts
df["score_reviews"] = df["reviews"].apply(score_authenticity)
df["score_menu"] = df["menu"].apply(score_authenticity)
df["score_decor"] = df["decor"].apply(score_authenticity)
df["authenticity_score"] = (
    0.4 * df["score_reviews"] +
    0.4 * df["score_menu"] +
    0.2 * df["score_decor"]
).round(2)

# Convertir en pourcentage
df["score_reviews_pct"] = (df["score_reviews"] * 20).round(2)
df["score_menu_pct"] = (df["score_menu"] * 20).round(2)
df["score_decor_pct"] = (df["score_decor"] * 20).round(2)
df["authenticity_score_pct"] = (df["authenticity_score"] * 20).round(2)

# Sauvegarder
df.to_csv("/home/manda/Téléchargements/MITL2/RESTAURANTS/restaurants_scored_n.csv", index=False)
print(f"\nScores d’authenticité pour {len(df)} restaurants (en %) :")
print(df[["name", "score_reviews_pct", "score_menu_pct", "score_decor_pct", "authenticity_score_pct"]])

# Étape 2 : Générer graphe (scores bruts pour NetworkX)
G = nx.Graph()
nodes = ["Nom", "Décor", "Menu", "Avis"]
G.add_nodes_from(nodes)
edges = [
    ("Menu", "Avis", 0.7),
    ("Nom", "Décor", 0.5),
    ("Menu", "Décor", 0.4),
    ("Avis", "Décor", 0.3)
]
G.add_weighted_edges_from(edges)

def simplify_key(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name).strip('_')

for i, row in df.iterrows():
    restaurant = row["name"]
    simplified_key = simplify_key(restaurant)
    for node in nodes:
        G.nodes[node]["label"] = node
        G.nodes[node][f"{simplified_key}_name"] = restaurant
        G.nodes[node][f"{simplified_key}_score"] = (
            1 if any(kw in restaurant.lower() for kw in ["chine", "jasmin", "saïgon", "dynastie"]) else 0 if node == "Nom" else
            row["score_decor"] if node == "Décor" else
            row["score_menu"] if node == "Menu" else
            row["score_reviews"]
        )

nx.write_gml(G, "/home/manda/Téléchargements/MITL2/RESTAURANTS/graphe_scores_n.gml")
print(f"Fichier graphe_scores_n.gml généré pour {len(df)} restaurants")

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1000, font_size=12)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)})
plt.title(f"Graphe pour {len(df)} restaurants")
plt.savefig("/home/manda/Téléchargements/MITL2/RESTAURANTS/graphe_n.png")
plt.close()

# Étape 3 : Générer rapport
pdf = SimpleDocTemplate(f"/home/manda/Téléchargements/MITL2/RESTAURANTS/rapport_authenticite_{len(df)}.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph(f"Analyse de l’authenticité de {len(df)} restaurants à Antananarivo", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph(
    f"Ce rapport évalue l’authenticité de {len(df)} restaurants à Antananarivo via un graphe et un agent IA.",
    styles["Normal"]
))
story.append(Spacer(1, 12))
story.append(Paragraph(
    f"Méthode : Graphe (NetworkX) avec nœuds Nom, Décor, Menu, Avis, sauvegardé dans graphe_scores_n.gml. "
    "Agent NLP (spaCy) analyse menu, reviews, décor (mots-clés : chinois, dim sum, lanternes, pho). "
    "Scores en pourcentage (sur 100%).",
    styles["Normal"]
))
story.append(Spacer(1, 12))
story.append(Paragraph("Résultats :", styles["Heading2"]))
data = [["Restaurant", "Avis (%)", "Menu (%)", "Décor (%)", "Authenticité (%)"]]
for _, row in df.iterrows():
    data.append([
        row["name"],
        f"{row['score_reviews_pct']:.2f}",
        f"{row['score_menu_pct']:.2f}",
        f"{row['score_decor_pct']:.2f}",
        f"{row['authenticity_score_pct']:.2f}"
    ])
table = Table(data)
table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, "black"), ("BACKGROUND", (0, 0), (-1, 0), "lightgrey")]))
story.append(table)
try:
    story.append(Image("/home/manda/Téléchargements/MITL2/RESTAURANTS/graphe_n.png", width=200, height=150))
except:
    story.append(Paragraph("Graphe non disponible", styles["Normal"]))
story.append(Spacer(1, 12))
top_restaurant = df.loc[df["authenticity_score_pct"].idxmax(), "name"]
story.append(Paragraph(
    f"Conclusion : {top_restaurant} est le plus authentique (score : {df['authenticity_score_pct'].max():.2f}%). "
    "Limites : Données partielles pour certains restaurants, URLs placeholders. "
    "Source visuelle (Le Jasmin) : <a href='https://www.facebook.com/photo/?fbid=912895374178628'>Facebook</a>.",
    styles["Normal"]
))
pdf.build(story)
print(f"Rapport généré : rapport_authenticite_{len(df)}.pdf")

# Étape 4 : Archiver
os.makedirs("/home/manda/Téléchargements/MITL2/RESTAURANTS/projet_restaurants", exist_ok=True)
files = [
    "restaurants_selected_n.csv",
    "restaurants_scored_n.csv",
    "graphe_scores_n.gml",
    "graphe_n.png",
    f"rapport_authenticite_{len(df)}.pdf"
]
for f in files:
    try:
        shutil.copy(
            f"/home/manda/Téléchargements/MITL2/RESTAURANTS/{f}",
            f"/home/manda/Téléchargements/MITL2/RESTAURANTS/projet_restaurants/{f}"
        )
    except FileNotFoundError:
        print(f"Fichier {f} manquant")
if os.path.exists("/home/manda/Téléchargements/MITL2/RESTAURANTS/images"):
    shutil.copytree(
        "/home/manda/Téléchargements/MITL2/RESTAURANTS/images",
        "/home/manda/Téléchargements/MITL2/RESTAURANTS/projet_restaurants/images",
        dirs_exist_ok=True
    )
print("Archivage terminé : projet_restaurants/")
