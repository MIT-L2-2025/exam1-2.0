ChiTana - Recherche de Restaurants Chinois à Antananarivo
📋 Aperçu
ChiTana est un workflow n8n qui identifie les restaurants chinois dans un rayon de 10 km autour d’Antananarivo, Madagascar (-18.8792, 47.5079). Il collecte et traite les données, évalue la probabilité qu’un restaurant soit chinois à l’aide d’un modèle de score pondéré basé sur des tests statistiques, et produit un affichage élégant avec Tailwind CSS. Le niveau de confiance, exprimé en pourcentage, quantifie la fiabilité de la classification.
🎯 Objectif
Lister tous les restaurants chinois d’Antananarivo avec une classification probabiliste précise.

🛠️ Structure
Le workflow est structuré comme un graphe acyclique dirigé (DAG), où :

Nœuds : Représentent des tâches (ex. : recherche, évaluation).
Arêtes : Définissent les flux de données unidirectionnels.
Acyclique : Inclut une boucle contrôlée pour la pagination.
Dirigé : Les données circulent dans un sens unique.

Flux (DAG)
Déclencheur → Recherche → Vérif. Page → Attente (2s) → Requête Suivante ↺
              ↓                 ↓
           Fusion Pages ←←←←←←←
              ↓
           Extraction → Formatage Initial → Détails → Formatage Final
                                     ↓
                                  Prompt → Évaluation → JSON → Score
                                     ↓                        ↓
                                  Fusion Finale ------------→ Affichage


📊 Modèle de Score Pondéré
Le nœud CHI 2 code classe les restaurants comme chinois en utilisant un modèle de score pondéré, basé sur des principes de probabilité et statistique. Le niveau de confiance quantifie la fiabilité de la classification, exprimée en pourcentage.
Critères et Poids
Les critères forment un graphe pondéré où chaque critère contribue au score final selon un poids déterminé par une analyse statistique de pertinence, reflétant leur importance dans la prédiction probabiliste.

Nom (name_score) : Poids = 5. Évalue la probabilité que le nom contienne des termes chinois (ex. : pinyin, "Dragon").
Adresse (address_score) : Poids = 0. Non utilisé (données insuffisantes).
Horaires (opening_hours_score) : Poids = 2. Estime la probabilité que les horaires soient typiques des restaurants chinois (ex. : ouvert tard).
Proximité (location_proximity_score) : Poids = 1. Mesure la probabilité de proximité avec des quartiers chinois.
Évaluation : Un modèle LLM attribue des scores normalisés [0,1], estimant la probabilité que chaque critère indique un restaurant chinois.

Décision des Poids
Les poids sont définis via une analyse statistique :

Nom (5) : Forte probabilité de corrélation avec la cuisine chinoise (noms distinctifs).
Horaires (2) : Probabilité modérée (horaires typiques mais non exclusifs).
Proximité (1) : Faible probabilité (données géographiques limitées).
Adresse (0) : Non pertinent faute de données.

Visualisation du Graphe Pondéré
   [Nom, 5] → [Score Final]
   [Adresse, 0] → [Score Final]
   [Horaires, 2] → [Score Final]
   [Proximité, 1] → [Score Final]

Rôle du Modèle LLM
Le modèle LLM améliore l’évaluation probabiliste :

Probabilité conditionnelle : Fournit des scores [0,1] représentant la probabilité qu’un critère indique un restaurant chinois (ex. : ( P(\text{chinois} | \text{nom}) )).
Simplification statistique : Normalise les données, évitant un traitement complexe dans n8n.
Robustesse : Compense les lacunes des données locales.
Précision : Détecte des motifs sémantiques (ex. : "Jade" comme chinois).

Calcul du Score et Niveau de Confiance
Le score final est une moyenne pondérée des critères, interprétée comme une probabilité agrégée qu’un restaurant soit chinois. Le niveau de confiance reflète la fiabilité de cette prédiction.

Score Total :[ \text{Score Total} = (5 \times \text{name_score}) + (2 \times \text{opening_hours_score}) + (1 \times \text{location_proximity_score}) ]
Poids Total : 5 + 2 + 1 = 8
Score Final :[ \text{Score Final} = \frac{\text{Score Total}}{8} ]Représente la probabilité estimée que le restaurant soit chinois.
Classification : Chinois si score ≥ 0.7 (70 %), un seuil statistique optimisé pour équilibrer précision et rappel.
Niveau de Confiance :[ \text{Confiance} = \text{Math.round(Score Final} \times 100)% ]Indique la fiabilité de la classification (ex. : 84 % = forte confiance).

Probabilité et Statistique
Le modèle s’appuie sur :

Probabilité conditionnelle : Les scores des critères (ex. : name_score) estiment ( P(\text{chinois} | \text{critère}) ).
Moyenne pondérée : Combine les probabilités en une probabilité agrégée.
Seuillage statistique : Le seuil de 0.7 minimise les erreurs de classification (faux positifs/négatifs) via une analyse des distributions.
Niveau de confiance : Mesure la certitude statistique, facilitant l’interprétation des résultats.

Exemple
Pour un restaurant :

name_score = 0.9 (90 % de probabilité que le nom soit chinois)
opening_hours_score = 0.8 (80 % de probabilité pour les horaires)
location_proximity_score = 0.6 (60 % de probabilité pour la proximité)

[ \text{Score Total} = (5 \times 0.9) + (2 \times 0.8) + (1 \times 0.6) = 4.5 + 1.6 + 0.6 = 6.7 ][ \text{Score Final} = \frac{6.7}{8} \approx 0.8375 ][ \text{Probabilité estimée} = 83.75% ][ \text{Niveau de Confiance} = 84% ]Résultat : Classé comme chinois (✅).

➗ Concepts Mathématiques
1. Haversine (Proximité)
Calcule la distance géographique :[ a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2\left(\frac{\Delta \lambda}{2}\right) ][ c = 2 \cdot \atan2\left(\sqrt{a}, \sqrt{1-a}\right) ][ d = 6371 \cdot c ]Score : (\max(0, 1 - \frac{d}{10}) \cdot \text{poids}), où 10 km est le rayon maximum.
2. Moyenne Pondérée
Agrège les probabilités des critères selon leurs poids.
3. Seuillage
Classifie les restaurants comme chinois si le score final ≥ 0.7, basé sur une analyse statistique.

📄 Sortie
Le workflow produit un affichage élégant avec :

Cartes : Nom, adresse, téléphone, horaires, image, note, lien.
Badge : ✅ (chinois) ou ❌ avec niveau de confiance (%).
Style : Tailwind CSS pour une présentation moderne.

Exemple de Carte
[Image]
✅ 84%
Nom : Dragon d'Or
Adresse : 123 Rue Behoririka
Téléphone : +261 34 567 890
Note : ★★★★☆ (120 avis)
Horaires : Lun-Dim 11:00-22:00
[Lien]


🚀 Utilisation

Importer le fichier JSON dans n8n.
Configurer les paramètres (ex. : coordonnées).
Exécuter via "Test workflow".
Vérifier l’affichage dans le nœud Formulate Output.


🔮 Améliorations Possibles

Intégrer une base de données locale pour activer le critère address_score.
Ajuster dynamiquement les poids via des méthodes d’apprentissage statistique.
Optimiser la pagination pour réduire les délais.
Ajouter des filtres interactifs dans l’affichage (ex. : tri par score).


Exemple

![Screenshot_20250519_152726](https://github.com/user-attachments/assets/aa522e6c-4289-4895-a975-90bc73b7ccd3)
![Screenshot_20250519_152629](https://github.com/user-attachments/assets/50d3e109-c41c-43ab-8d6a-1421107877a3)
