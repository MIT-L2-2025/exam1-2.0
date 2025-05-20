from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

# Charger données
df = pd.read_csv("restaurants_scored.csv")

# Créer PDF
pdf = SimpleDocTemplate("rapport_authenticite.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Titre
story.append(Paragraph("Analyse de l’authenticité des restaurants chinois à Antananarivo", styles["Title"]))
story.append(Spacer(1, 12))

# Introduction
story.append(Paragraph(
    "Ce rapport évalue l’authenticité de deux restaurants supposés chinois à Antananarivo "
    "en analysant leurs noms, menus, avis clients, et décor à l’aide d’un graphe et d’un agent IA.",
    styles["Normal"]
))
story.append(Spacer(1, 12))

# Méthode
story.append(Paragraph(
    "Méthode : Un graphe (NetworkX) modélise les relations entre Nom, Décor, Menu, et Avis "
    "(arêtes pondérées : Menu→Avis 0.7, Nom→Décor 0.5, etc.). Un agent NLP (spaCy) analyse "
    "les données avec des mots-clés (ex. : ‘chinois’, ‘dim sum’, ‘lanternes’). Scores : "
    "reviews (40%), menu (40%), décor (20%).",
    styles["Normal"]
))
story.append(Spacer(1, 12))

# Résultats
story.append(Paragraph("Résultats :", styles["Heading2"]))
data = [["Restaurant", "Score Reviews", "Score Menu", "Score Décor", "Authenticité"]]
for _, row in df.iterrows():
    data.append([
        row["name"], row["score_reviews"], row["score_menu"],
        row["score_decor"], row["authenticity_score"]
    ])
table = Table(data)
table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 1, "black"),
    ("BACKGROUND", (0, 0), (-1, 0), "lightgrey"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER")
]))
story.append(table)
story.append(Spacer(1, 12))

# Conclusion
top_restaurant = df.loc[df["authenticity_score"].idxmax(), "name"]
story.append(Paragraph(
    f"Conclusion : {top_restaurant} est le plus authentique (score : {df['authenticity_score'].max()}). "
    "Limites : URLs d’images placeholders, données limitées pour Le Jasmin. "
    "Source visuelle : <a href='https://scontent.ftnr2-2.fna.fbcdn.net/v/t39.30808-6/494032931_1212669274201235_7941012071558718_n.jpg?stp=cp6_dst-jpg_tt6&_nc_cat=102&ccb=1-7&_nc_sid=cc71e4&_nc_ohc=jOqDhydEl_oQ7kNvwHYoVgP&_nc_oc=Adk6wYsZJqCARS3hS6wkKS8PRwIXX1hLKWE6AspZwIbslUS_X3H9ivU8eSNt-acYSsg&_nc_zt=23&_nc_ht=scontent.ftnr2-2.fna&_nc_gid=ewR9LI773deS-ZlwC_1p9Q&oh=00_AfL6PMZaxPNoIIqsQPqSteeU5ZCvduLcHRIkl7P2B0wIcw&oe=6830B88D'>Le Jasmin</a>.",
    styles["Normal"]
))

# Générer PDF
pdf.build(story)
print("Rapport généré : rapport_authenticite.pdf")
