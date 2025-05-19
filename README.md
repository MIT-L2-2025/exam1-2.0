# 🌟 Classification des Restaurants avec la Théorie des Graphes

Ce projet utilise la **théorie des graphes** pour classer les restaurants d'Antananarivo comme **Chinois**, **Modérément Chinois** ou **Non Chinois**, en s'appuyant sur un système de scores pondérés. Voici comment les graphes transforment des données brutes en une analyse puissante et visuelle !

## 🎯 Modélisation du Graphe

Les restaurants sont représentés comme un **graphe non orienté pondéré** \( G = (V, E, w) \) :
- **Sommets (\( V \))** : Les restaurants, avec des attributs comme le nom, les coordonnées GPS, et la spécialité.
- **Arêtes (\( E \))** : Les relations de proximité géographique, basées sur la **distance Haversine**, reliant chaque restaurant à ses 5 voisins les plus proches.
- **Poids (\( w \))** : Dépendent de la distance :
  | Distance (\( d \)) | Poids (\( w_d \)) |
  |--------------------|-------------------|
  | \( d < 1 \, \text{km} \) | 0.4 |
  | \( 1 \leq d < 5 \, \text{km} \) | 0.2 |
  | \( d \geq 5 \, \text{km} \) | 0.1 |

## 🧮 Scores de Classification

Le nœud `classifyRestaurants` calcule un **score total** pour chaque restaurant à partir de 5 scores pondérés, combinant des propriétés intrinsèques et relationnelles :

| Score | Description | Formule | Rôle dans le Graphe |
|-------|-------------|---------|---------------------|
| \( s_1 \) | Nom contient des mots-clés chinois (ex. : "dragon") ou asiatiques (ex. : "jade") | 1.0 (chinois), 0.5 (asiatique), 0.0 (autre) | Propriété du sommet |
| \( s_2 \) | Influence des 5 voisins les plus proches | \( \frac{1}{5} \sum \text{score}_1(\text{voisin}) \cdot w_d \) | Sous-graphe local (arêtes pondérées) |
| \( s_3 \) | Proximité des quartiers chinois | Basé sur la distance Haversine et le poids du quartier | Connexion à des "sommets fictifs" (quartiers) |
| \( s_4 \) | Spécialité chinoise ou asiatique | Similaire à \( s_1 \) | Propriété du sommet |
| \( s_5 \) | Interaction nom-proximité | \( s_5 = s_1 \cdot s_3 \) | Interaction sommet-quartier |

**Score Total** :
\[
\text{score_total} = 0.30 \cdot s_1 + 0.05 \cdot s_2 + 0.15 \cdot s_3 + 0.30 \cdot s_4 + 0.20 \cdot s_5
\]

**Classification** :
| Score Total | Classification |
|-------------|---------------|
| \( \geq 0.6 \) | Chinois |
| \( [0.25, 0.6) \) | Modérément Chinois |
| \( < 0.25 \) | Non Chinois |

## 🚀 Rôle de la Théorie des Graphes

- **Graphe de Proximité** : Le score \( s_2 \) crée un sous-graphe local où chaque restaurant est connecté à ses 5 voisins les plus proches, avec des arêtes pondérées par la distance Haversine. Cela reflète une **propagation d'étiquettes** : un restaurant proche de restaurants chinois a plus de chances d'être chinois.
- **Quartiers Chinois** : Les quartiers agissent comme des points de référence, formant un graphe bipartite implicite avec les restaurants.
- **Segmentation** : La classification finale divise le graphe en trois sous-ensembles, comme une partition basée sur les scores.

