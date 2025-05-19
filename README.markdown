# 🥡 ChiTana — Restaurants Chinois à Antananarivo

**ChiTana** est un workflow **n8n** qui identifie les restaurants chinois dans un rayon de 10 km autour d’**Antananarivo, Madagascar** (`-18.8792, 47.5079`). Il collecte, analyse et classe les données selon un **modèle probabiliste pondéré**, puis les affiche dans une interface élégante avec **Tailwind CSS**.
Chaque restaurant reçoit un **score de probabilité (%)** indiquant la fiabilité de sa classification.

---

## 🎯 Objectif

> Fournir une **liste fiable** et **classée** des restaurants chinois d’Antananarivo à l’aide de critères statistiques.

---

## ⚙️ Architecture du Workflow

ChiTana est structuré comme un **graphe acyclique dirigé (DAG)** :

* **Nœuds** : tâches de recherche, extraction, évaluation, etc.
* **Arêtes** : flux de données unidirectionnels.
* **Acyclique** : boucle contrôlée pour gérer la pagination.
* **Dirigé** : circulation unique de l’information.

### 🔁 Schéma du Flux (DAG)

```
Déclencheur → Recherche → Vérif. Page → Attente (2s) → Requête Suivante ↺
                  ↓               ↓
               Fusion Pages ←←←←←←
                  ↓
               Extraction → Formatage Initial → Détails → Formatage Final
                                             ↓
                                          Prompt → Évaluation → Score et test probabiliste
                                             ↓                        ↓
                                          Fusion Finale ------------→ Affichage
```

---

## 📊 Modèle de Score Pondéré

Chaque restaurant est évalué à partir de **critères pondérés**. Ces critères sont combinés pour produire un **score final** (de 0 à 1), reflétant la **probabilité estimée** qu’il s’agisse d’un restaurant chinois.

### 🔎 Critères & Poids

| Critère                    | Description                                             | Poids |
| -------------------------- | ------------------------------------------------------- | ----- |
| `name_score`               | Analyse du nom (pinyin, "Dragon", etc.)                 | 5     |
| `opening_hours_score`      | Évalue si les horaires sont typiques des restos chinois | 2     |
| `location_proximity_score` | Proximité avec des quartiers à forte densité chinoise   | 1     |
| `address_score`            | Non utilisé (données insuffisantes)                     | 0     |

> 💡 Les poids sont définis manuelement ou via une **analyse statistique de corrélation** (importance relative des critères dans la prédiction).

### 🧠 Rôle du LLM

Un modèle de langage (LLM) attribue des scores normalisés `[0,1]` :

* **Probabilité conditionnelle** : P(chinois | critère)
* **Normalisation** : simplifie le traitement dans n8n
* **Robustesse** : compense le manque de données local et structurées
* **Précision** : détecte des motifs sémantiques (ex. : "Jade", "Mandarin")

---

## 🧮 Calcul du Score Final

```text
Score Total   = (5 × name_score) + (2 × opening_hours_score) + (1 × location_proximity_score)
Score Final   = Score Total / (5 + 2 + 1)
Niveau de Confiance = Score Final × 100 (%)
```
Ou les `{5,2,1}` sont les poids 
### ✅ Classification

* **Chinois** : Score Final ≥ **0.7** (70 %)
* **Confiance** : Arrondie au pourcentage, ex. 83.75 % → 84 %

> 📐 Le seuil de 0.7 est défini via une **analyse de distribution** pour équilibrer **précision et rappel**.

---

## 🔢 Exemple

```text
name_score = 0.9
opening_hours_score = 0.8
location_proximity_score = 0.6

Score Total = (5×0.9) + (2×0.8) + (1×0.6) = 6.7
Score Final = 6.7 / 8 ≈ 0.8375
Confiance = 84 %
✅ Classé comme chinois
```

---

## Concepts Mathématiques

1. **Distance (Haversine)**
Utile pour savoir si le lieu de la restaurant est inclus dans la zone a forte densite de chinois a Antananarivo (ex:.Behoririka,..)
   ```text
   d = 6371 × 2 × atan2(√a, √(1−a))
   a = sin²(Δφ/2) + cos(φ1) × cos(φ2) × sin²(Δλ/2)
   Score = max(0, 1 − d / 10)
   ```
2. **Moyenne Pondérée**
   Utilisée pour agréger les scores selon leur poids.
3. **Seuillage Statistique**
   Le seuil de 0.7 maximise la qualité de classification (évite les faux positifs/négatifs).

---

## 📄 Affichage

Le résultat final est présenté via une **UI responsive (Tailwind CSS)** avec :

* **Cartes** : nom, adresse, téléphone, horaires, image, avis, lien.
* **Badge** : ✅ ou ❌ avec score de confiance.
* **Design moderne**, clair et mobile-friendly.

### 📸 Exemple de carte

![Screenshot](https://github.com/user-attachments/assets/aa522e6c-4289-4895-a975-90bc73b7ccd3)
![Screenshot](https://github.com/user-attachments/assets/50d3e109-c41c-43ab-8d6a-1421107877a3)

---

## 🚀 Utilisation

1. Importer le fichier `.json` dans **n8n**.
2. Lancer via **“Test Workflow”**.
3. Consulter le résultat dans le nœud **Formulate Output**.

---

## 🌱 Améliorations Futures

* Ajouter une **base de données locale** pour activer le `address_score`.
* Optimiser les poids via des **méthodes d’apprentissage automatique**.

---

## 📌 Résumé

**ChiTana** combine :
🔍 collecte intelligente · 📊 analyse statistique · 🤖 IA sémantique · 🎨 UI moderne
… pour vous offrir un **classement fiable** des restaurants chinois à Antananarivo.
---
