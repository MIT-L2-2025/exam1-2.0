# 🌟 Classification des Restaurants avec la Théorie des Graphes

Ce projet utilise la **théorie des graphes** pour classer les restaurants d'Antananarivo comme **Chinois**, **Modérément Chinois** ou **Non Chinois**, en s'appuyant sur un système de scores pondérés. Voici comment les graphes transforment des données brutes en une analyse puissante et visuelle !

---

## 🎯 Modélisation du Graphe

Les restaurants sont représentés comme un **graphe non orienté pondéré** \( G = (V, E, w) \) :

- **Sommets (\( V \))** : Représentent les restaurants, avec des attributs comme :
  - Nom
  - Coordonnées GPS
  - Spécialité

- **Arêtes (\( E \))** : Relations de proximité géographique, basées sur la **distance Haversine**, connectant chaque restaurant à ses **5 voisins les plus proches**.

- **Poids (\( w \))** : Pondération basée sur la distance :

| Distance (\( d \))          | Poids (\( w_d \)) |
|----------------------------|-------------------|
| \( d < 1 \, \text{km} \)   | 0.4               |
| \( 1 \leq d < 5 \, \text{km} \) | 0.2          |
| \( d \geq 5 \, \text{km} \) | 0.1               |

---

## 🧮 Scores de Classification

Le nœud `classifyRestaurants` calcule un **score total** pour chaque restaurant à partir de 5 scores partiels, combinant des propriétés **intrinsèques** et **relationnelles** :

| Score | Description | Formule | Rôle dans le Graphe |
|-------|-------------|---------|---------------------|
| \( s_1 \) | Nom contient des mots-clés chinois (ex. : "dragon") ou asiatiques (ex. : "jade") | 1.0 (chinois), 0.5 (asiatique), 0.0 (autre) | Propriété du sommet |
| \( s_2 \) | Influence des 5 voisins les plus proches | \( \frac{1}{5} \sum \text{score}_1(\text{voisin}) \cdot w_d \) | Sous-graphe local |
| \( s_3 \) | Proximité aux quartiers chinois | Pondérée par la distance Haversine | Connexion à des nœuds "quartiers" |
| \( s_4 \) | Spécialité chinoise ou asiatique | Même logique que \( s_1 \) | Propriété du sommet |
| \( s_5 \) | Interaction nom–proximité | \( s_5 = s_1 \cdot s_3 \) | Interaction sommet–quartier |

### 📊 Formule du Score Total

\[
\text{score_total} = 0.30 \cdot s_1 + 0.05 \cdot s_2 + 0.15 \cdot s_3 + 0.30 \cdot s_4 + 0.20 \cdot s_5
\]

### 🧾 Classification

| Score Total           | Classification         |
|-----------------------|------------------------|
| \( \geq 0.6 \)        | 🟥 Chinois              |
| \( [0.25, 0.6) \)     | 🟦 Modérément Chinois   |
| \( < 0.25 \)          | 🟩 Non Chinois          |

---

## 🚀 Rôle de la Théorie des Graphes

- **Graphe de Proximité** : Le score \( s_2 \) reflète une forme de **propagation d’étiquette** — un restaurant proche de restaurants chinois a plus de chances d’être lui-même chinois.
- **Quartiers Chinois** : Ajoutés comme nœuds fictifs, ils permettent une analyse **bipartite** implicite entre restaurants et quartiers.
- **Segmentation** : La classification finale forme une **partition du graphe** en trois sous-ensembles (Chinois, Modérément Chinois, Non Chinois).

---

## 🗺️ Visualisation : Restaurants Fictifs à Antananarivo

Visualisation 2D interactive d'un graphe de **9 restaurants fictifs** :

### 🔴 Chinois (score ≥ 0.6)

- Lotus (0.7)  
- Dragon (0.8)  
- Panda (0.9)

### 🔵 Modérément Chinois (0.25 ≤ score < 0.6)

- Jade (0.4)  
- Bamboo (0.5)  
- Orchid (0.6)

### 🟢 Non Chinois (score < 0.25)

- Soleil (0.1)  
- Étoile (0.2)  
- Lune (0.3)

### 🔗 Arêtes

- Chaque nœud connecté à **2 voisins les plus proches** (selon distance Haversine)
- **Poids** :
  - 0.4 si \( < 1 \) km
  - 0.2 si entre 1–5 km
  - 0.1 si \( \geq 5 \) km

### 🧭 Fonctionnalités

- **Disposition** : `spring_layout` (force dirigée)
- **Taille des nœuds** : \( \text{score_total} \cdot 30 + 10 \)
- **Étiquettes** : nom, score, classification
- **Infobulles** interactives
- **Drag-and-drop** des nœuds
- **Canvas** 600x500, avec légende et grille
- **Export** possible (.ps ou image)

---
