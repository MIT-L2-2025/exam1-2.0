import pandas as pd
import spacy

# Charger spaCy
nlp = spacy.load("fr_core_news_sm")
keywords = [
    "authentique", "chinois", "dim sum", "tsa-siou", "kung pao", "sichuan",
    "cantonnais", "lanternes", "calligraphie", "dragon", "aigre-doux",
    "chow mein", "nems", "cuisine chinoise", "vapeur", "soupes"
]

# Charger CSV
df = pd.read_csv("restaurants_selected.csv")

# Afficher données sources
print("Données sources :")
for _, row in df.iterrows():
    print(f"\nRestaurant : {row['name']}")
    print(f"Menu : {row['menu']}")
    print(f"Reviews : {row['reviews']}")
    print(f"Décor : {row['decor']}")

# Fonction pour scorer (améliorée)
def score_authenticity(texts):
    if not texts or texts == "":
        return 0
    score = 0
    texts = eval(texts) if isinstance(texts, str) and texts.startswith("[") else [texts]
    for text in texts:
        text = str(text).lower()
        doc = nlp(text)
        # Compter mots-clés exacts + sous-chaînes
        score += sum(1 for token in doc if token.text in keywords)
        score += sum(1 for kw in keywords if kw in text and kw not in [token.text for token in doc])
    return min(score, 5)

# Recalculer scores
df["score_reviews"] = df["reviews"].apply(score_authenticity)
df["score_menu"] = df["menu"].apply(score_authenticity)
df["score_decor"] = df["decor"].apply(score_authenticity)
df["authenticity_score"] = (
    0.4 * df["score_reviews"] +
    0.4 * df["score_menu"] +
    0.2 * df["score_decor"]
).round(2)

# Sauvegarder
df.to_csv("restaurants_scored.csv", index=False)
print("\nScores recalculés :")
print(df[["name", "score_reviews", "score_menu", "score_decor", "authenticity_score"]])
