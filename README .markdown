# README - Analyse des Restaurants Chinois à Antananarivo

## Aperçu
Ce projet utilise un flux de travail n8n pour analyser et lister les restaurants chinois à Antananarivo, Madagascar. Il collecte des données sur 41 restaurants, calcule la probabilité qu'ils soient chinois, effectue un test statistique Khi-deux, et génère un rapport HTML interactif.

## Fonctionnalités
- **Données** : Liste de 41 restaurants avec nom, adresse, type de cuisine, menu, téléphone, et URL d'image.
- **Analyse** : Calcule une probabilité (en %) qu'un restaurant soit chinois basée sur des critères comme le nom, le menu, et la présence de caractères chinois.
- **Statistiques** : Test Khi-deux pour évaluer la corrélation entre les caractéristiques chinoises et la classification.
- **Sortie** : Génère un fichier HTML (`chinese_restaurants_antananarivo.html`) avec une liste des restaurants probables (probabilité > 70 %), leurs détails, et des liens Google Maps.

## Structure du Flux
1. **Start** : Déclenche le flux.
2. **Function - Données Restaurants** : Charge les données des restaurants.
3. **Function - Calcul Probabilité** : Calcule la probabilité et prépare les données pour le test Khi-deux.
4. **Function - Générer HTML** : Crée un rapport HTML avec les résultats.
5. **Write Binary File** : Sauvegarde le rapport dans `chinese_restaurants_antananarivo.html`.

## Résultats
- **Restaurants analysés** : 41
- **Restaurants probables chinois** : 26 (probabilité > 70 %)
- **Probabilité moyenne** : 90 %
- **Test Khi-deux** : Valeur = 2.99, p = 0.776 (aucune corrélation significative).

## Prérequis
- **n8n** : Plateforme d'automatisation pour exécuter le flux.
- **Fichier JSON** : `My_workflow_.json` contient le flux de travail.
- **Sortie** : Le fichier HTML généré nécessite un navigateur pour visualisation.

## Utilisation
1. Importez `My_workflow_.json` dans n8n.
2. Exécutez le flux.
3. Consultez le fichier `chinese_restaurants_antananarivo.html` pour les résultats.

## Notes
- Les données sont statiques et basées sur une liste prédéfinie.
- Les liens Google Maps sont générés à partir des adresses fournies.
- Le test Khi-deux utilise une approximation pour la p-valeur.

## Avertissement
Ce projet est une analyse automatisée et les résultats dépendent de la qualité des données d'entrée. Vérifiez les informations avant utilisation.