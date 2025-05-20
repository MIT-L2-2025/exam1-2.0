# Analyse des Restaurants Chinois à Antananarivo

Utilisation du n8n pour analyser 41 restaurants à Antananarivo, identification de ceux qui sont chinois avec un test statistique Khi-deux, et aussi générer un rapport HTML interactif.

## Fonctionnalités
- **Collecte des données** : Liste de 41 restaurants avec nom, adresse, téléphone, type de cuisine, et menu.
- **Analyse statistique** : Calcul de la probabilité qu’un restaurant soit chinois et test Khi-deux pour vérifier la corrélation.
- **Sortie HTML** : Page web avec une liste des restaurants probables, leurs détails, et des liens Google Maps.

## Structure du Workflow
- **Function - Données Restaurants** : Fournit les données des restaurants.
- **Function - Calcul Probabilité** : Calcule la probabilité et prépare le test Khi-deux.
- **Function - Générer HTML** : Crée le contenu HTML.
- **Debug Binary Data** : Vérifie les données binaires.
- **Output HTML** : Affiche le HTML pour copie manuelle.

## Résultats
- Fichier : `chinese_restaurants_antananarivo.html`
- Affiche les restaurants avec une probabilité > 70% d’être chinois, avec statistiques et tableau Khi-deux.

## Prérequis
- n8n (version récente, installé via Docker).
- Navigateur web pour visualiser le HTML.

## Utilisation
1. Importer `My_workflow_.json` dans n8n.
2. Exécuter le workflow.
3. Copier la valeur `html_output` depuis le nœud **Output HTML**.
4. Sauvegarder comme `chinese_restaurants_antananarivo.html` et ouvrir dans un navigateur.
