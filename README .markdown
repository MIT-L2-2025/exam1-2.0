# README - Analyse des Restaurants Chinois à Antananarivo


Utilisation d'un flux de travail n8n pour analyser et lister les restaurants chinois à Antananarivo. Il collecte des données sur 41 restaurants, calcule la probabilité qu'ils soient chinois, effectue un test statistique Khi-deux, et génère un rapport HTML interactif.

## Fonctionnalités
- **Données** : Liste de 41 restaurants avec nom, adresse, type de cuisine, menu, téléphone, et URL d'image.
- **Analyse** : Calcule une probabilité (en %) qu'un restaurant soit chinois basée sur des critères comme le nom, le menu, et la présence de caractères chinois.
- **Statistiques** : Test Khi-deux pour évaluer la corrélation entre les caractéristiques chinoises et la classification.
- **Sortie** : Génère un fichier HTML (`Chinese_restaurants_antananarivo.html`) avec une liste des restaurants probables (probabilité > 70 %), leurs détails, et des liens Google Maps.

## Résultats
- **Restaurants analysés** : 41
- **Restaurants probables chinois** : 26 (probabilité > 70 %)
- **Probabilité moyenne** : 90 %
- **Test Khi-deux** : Valeur = 2.99, p = 0.776 (aucune corrélation significative).
