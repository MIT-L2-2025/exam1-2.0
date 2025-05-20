Liste des Restaurants Chinois à Antananarivo

Ce projet permet d'identifier les vrais restaurants chinois authentiques à Antananarivo, Madagascar. En utilisant des données récupérées et un filtrage statistique, j’ai compilé une liste fiable de ces restaurants.
Méthodologie

Récupération des données : J’ai utilisé une requête HTTP via l’API SerpAPI pour collecter des données sur les restaurants à Antananarivo (noms, adresses, coordonnées, types, avis, etc.).
Traitement des données : J’ai développé un workflow de traitement qui :
Évalue chaque restaurant selon des critères (nom, localisation dans un quartier chinois, type de cuisine, avis).
Applique un test de khi-deux (χ²) pour valider statistiquement la dépendance entre ces critères (ex. nom chinois et localisation).
Filtre les restaurants pour ne garder que ceux identifiés comme authentiquement chinois.

Structure du Projet
data/: Contient les données brutes récupérées via SerpAPI (JSON).
scripts/: Scripts de traitement et de filtrage (JavaScript, utilisés dans un workflow n8n).
output/: Liste finale des restaurants chinois authentiques (JSON).

Remarques
Le test de khi-deux m’a permis de m’assurer que les critères de filtrage (comme le nom et la localisation) sont statistiquement fiables.
