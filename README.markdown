# ChiTana - Recherche de Restaurants Chinois à Antananarivo

## 📋 Aperçu

**ChiTana** est un workflow n8n qui identifie les restaurants chinois dans un rayon de 10 km autour d’Antananarivo, Madagascar (-18.8792, 47.5079). Il collecte et traite les données, évalue la probabilité qu’un restaurant soit chinois à l’aide d’un modèle de score pondéré basé sur des tests statistiques, et génère une page HTML stylisée avec Tailwind CSS.

### 🎯 Objectif
Lister tous les restaurants chinois d’Antananarivo avec une classification précise.

---

## 🛠️ Structure

Le workflow est organisé en un **graphe acyclique dirigé (DAG)** :
- **Nœuds** : Tâches (ex. : recherche, évaluation).
- **Arêtes** : Flux de données entre tâches.

### Nœuds Principaux
1. **Déclencheur** : Initie le workflow.
2. **Recherche Initiale** : Collecte les restaurants associés au terme "chinois".
3. **Vérification Page Suivante** : Détecte les résultats supplémentaires.
4. **Attente** : Pause de 2 secondes pour respecter les limites d’API.
5. **Requête Suivante** : Récupère les pages suivantes.
6. **Fusion Pages** : Combine les résultats de toutes les pages.
7. **Extraction** : Extrait les données (nom, adresse, etc.).
8. **Formatage Initial** : Structure les données brutes.
9. **Détails** : Ajoute des informations (téléphone, photos).
10. **Formatage Final** : Prépare images, liens et horaires.
11. **Prompt** : Génère des prompts pour l’évaluation.
12. **Évaluation** : Attribue des scores via un modèle LLM.
13. **JSON** : Convertit les résultats en JSON.
14. **Score Pondéré** : Calcule le score final.
15. **Fusion Finale** : Combine données et scores.
16. **HTML** : Génère une page HTML avec Tailwind CSS.

### Flux (DAG)
```
Déclencheur → Recherche → Vérif. Page → Attente (2s) → Requête Suivante ↺
              ↓                 ↓
           Fusion Pages ←←←←←←←
              ↓
           Extraction → Formatage Initial → Détails → Formatage Final
                                     ↓
                                  Prompt → Évaluation → JSON → Score
                                     ↓                        ↓
                                  Fusion Finale ------------→ HTML
```

---

## 📊 Modèle de Score Pondéré

Le nœud `CHI 2 code` évalue si un restaurant est chinois à l’aide de tests statistiques et d’un modèle de score pondéré.

### Critères et Poids
Les critères forment un **graphe pondéré** où chaque critère (nœud) contribue au score final selon un poids déterminé par une analyse statistique de pertinence.

- **Nom (`name_score`)** : Poids = **5**. Analyse la présence de termes chinois (ex. : pinyin, caractères).
- **Adresse (`address_score`)** : Poids = **0**. Non utilisé (données insuffisantes).
- **Horaires (`opening_hours_score`)** : Poids = **2**. Vérifie les horaires typiques (ex. : ouvert tard).
- **Proximité (`location_proximity_score`)** : Poids = **1**. Mesure la distance aux quartiers chinois.
- **Évaluation** : Un **modèle LLM** attribue des scores normalisés [0,1] aux critères, simplifiant l’analyse sémantique et compensant l’absence de données locales.

#### Décision des Poids
Les poids reflètent l’importance relative des critères :
- **Nom (5)** : Très discriminant (noms chinois distinctifs).
- **Horaires (2)** : Indicateur secondaire (horaires typiques).
- **Proximité (1)** : Utile mais moins fiable (données géographiques limitées).
- **Adresse (0)** : Exclue faute de données exploitables.

#### Visualisation du Graphe Pondéré
```
   [Nom, 5] → [Score Final]
   [Adresse, 0] → [Score Final]
   [Horaires, 2] → [Score Final]
   [Proximité, 1] → [Score Final]
```

#### Pourquoi un Modèle LLM ?
- **Simplification** : Fournit des scores [0,1] sans traitement complexe de langage naturel dans n8n.
- **Fiabilité** : Compense le manque de données locales sur les restaurants chinois.
- **Précision** : Détecte des motifs sémantiques (ex. : "Dragon" comme chinois).
- **Efficacité** : Automatise l’évaluation, réduisant le besoin de règles manuelles.

### Calcul du Score
1. **Score Total** :  
   \[ \text{Score Total} = (5 \times \text{name_score}) + (2 \times \text{opening_hours_score}) + (1 \times \text{location_proximity_score}) \]
2. **Poids Total** : 5 + 2 + 1 = 8
3. **Score Final** :  
   \[ \text{Score Final} = \frac{\text{Score Total}}{8} \]
4. **Classification** : Restaurant chinois si score ≥ 0.7 (70 %).
5. **Confiance** : \(\text{Math.round(Score Final} \times 100)\%\).

### Exemple
Pour un restaurant :
- `name_score = 0.9`
- `opening_hours_score = 0.8`
- `location_proximity_score = 0.6`

\[ \text{Score Total} = (5 \times 0.9) + (2 \times 0.8) + (1 \times 0.6) = 4.5 + 1.6 + 0.6 = 6.7 \]  
\[ \text{Score Final} = \frac{6.7}{8} \approx 0.8375 \]  
\[ \text{Confiance} = 84\% \]  
**Résultat** : Chinois (✅).

---

## 🌐 Concepts de Graphe

Le workflow est un **DAG** :
- **Nœuds** : Tâches spécifiques.
- **Arêtes** : Flux de données unidirectionnels.
- **Acyclique** : Boucle contrôlée pour la pagination.
- **Dirigé** : Données transmises dans un seul sens.

---

### 1. Haversine (Proximité)
Calcule la distance géographique :  
\[ a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2\left(\frac{\Delta \lambda}{2}\right) \]  
\[ c = 2 \cdot \atan2\left(\sqrt{a}, \sqrt{1-a}\right) \]  
\[ d = 6371 \cdot c \]  
**Score** : \(\max(0, 1 - \frac{d}{10}) \cdot \text{poids}\), où 10 km est le rayon maximum.

### 2. Moyenne Pondérée
Agrège les scores des critères selon leurs poids.

### 3. Seuillage
Classifie les restaurants comme chinois si le score final ≥ 0.7.

---

## 📄 Sortie

Un fichier HTML (`restaurants_antananarivo.html`) est généré avec :
- **Cartes** : Nom, adresse, téléphone, horaires, image, note, lien.
- **Badge** : ✅ (chinois) ou ❌ avec pourcentage de confiance.

### Exemple de Carte
```
[Image]
✅ 84%
Nom : Dragon d'Or
Adresse : 123 Rue Behoririka
Téléphone : +261 34 567 890
Note : ★★★★☆ (120 avis)
Horaires : Lun-Dim 11:00-22:00
[Lien]
```

---

## 🚀 Utilisation
1. Importer le fichier JSON dans n8n.
3. Exécuter via "Test workflow".
4. Vérifier la sortie HTML dans le nœud `Formulate HTML`.

---

## 🔮 Exemple de html
![Screenshot_20250519_152726](https://github.com/user-attachments/assets/5a62d966-2b12-40b9-ba45-37d9f93b02b0)
![Screenshot_20250519_152629](https://github.com/user-attachments/assets/691ef6d6-a880-44cd-8fa6-31fe342582db)
