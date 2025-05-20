
# 🇨🇳 Restaurant Chinois Classifier 🍜🍱

Ce projet a pour but de **classifier automatiquement si un restaurant est chinois ou non**, en se basant sur **des images collectées depuis Google Places**, **stockées dans PostgreSQL via Railway**, et **analysées via le modèle CLIP** sur Google Colab.

---

## 🧠 Objectif

* Identifier automatiquement les **restaurants chinois** à partir de leurs **photos publiques** (plats, menus, lieux).
* Utiliser des outils modernes (APIs, IA, cloud) pour automatiser un pipeline complet de collecte, stockage et traitement des données.

---

## 📦 Pipeline du projet

### 1. 📊 **Collecte des données restaurants** – via **Apify**

* Utilisation de [Apify](https://apify.com/) pour extraire des **listes de restaurants** avec leurs **noms, adresses, coordonnées géographiques**, etc.
* Résultat : une base tabulaire de restaurants de la zone ciblée (par ex. Antananarivo).

---

### 2. 🖼️ **Scraping des images** – via **Google Places API**

* Pour chaque restaurant, appel à l’API **Google Places** pour récupérer des **photos associées** (menus, plats, lieux).
* Les images sont encodées en **base64** pour être stockées facilement en base de données.

---

### 3. 🗄️ **Stockage dans PostgreSQL** – via **[Railway](https://railway.app/)**

* Utilisation de **Railway**, une plateforme PaaS simple et puissante pour déployer et héberger une **base de données PostgreSQL dans le cloud**.
* Chaque image est stockée dans une table `photo`, avec :

  * `photo_data` (base64),
  * `restaurant_id`,
  * champs de classification (`photo_type`, `photo_chinois`, `proba_chinois`).

---

### 4. 🧪 **Traitement et classification des images** – via **Google Colab + CLIP**

* Utilisation de **Google Colab** (GPU gratuit) pour le traitement des images.
* Chargement du modèle **[CLIP (Contrastive Language–Image Pretraining)](https://github.com/openai/CLIP)** d'OpenAI.
* Deux étapes de classification :

#### ➤ a. 📸 *Type de photo* :
![plat1](https://github.com/user-attachments/assets/4b0824e0-1c63-4a23-8515-27ae7d490eb4)

```python
["PHOTO_PLAT", "PHOTO_MENU", "PHOTO_LIEU"]


Basé sur la similarité avec les descriptions textuelles :

```python
["un plat de nourriture", "une carte de menu", "un intérieur ou extérieur de restaurant"]
```

#### ➤ b. 🉐 *Est-ce chinois ou non ?*
![plat_chinois1](https://github.com/user-attachments/assets/d91e21a0-2fae-4102-ba21-6d827070f37a)

* Pour chaque type, les libellés changent :

  * Plat → \["un plat chinois", "un plat non chinois"]
  * Menu → \["un menu chinois", "un menu non chinois"]
  * Lieu → \["un lieu de restaurant chinois", "un lieu de restaurant non chinois"]
* CLIP retourne une **probabilité** d’être chinois (`proba_chinois`) pour chaque image.

---

### 5. 🧾 **Déduction du type de restaurant**

* Agrégation des photos par `restaurant_id` :

  * Si **au moins une photo est "chinoise"** et que la **moyenne des probabilités > 0.5**, alors le restaurant est classé comme **"chinois"**.
* Mise à jour de la colonne `is_chinois` dans la table `restaurant`.

---

## 📂 Structure de la base de données

### 📁 Table `restaurant`

| Champ       | Type    | Description                    |
| ----------- | ------- | ------------------------------ |
| id          | INTEGER | Identifiant du restaurant      |
| name        | TEXT    | Nom du restaurant              |
| address     | TEXT    | Adresse                        |
| ...         | ...     | Autres champs                  |
| is\_chinois | BOOLEAN | Classifié comme chinois ou non |

---

### 📁 Table `photo`

| Champ          | Type    | Description                        |
| -------------- | ------- | ---------------------------------- |
| id             | INTEGER | ID unique de la photo              |
| restaurant\_id | INTEGER | Clé étrangère vers `restaurant`    |
| photo\_data    | TEXT    | Image encodée en base64            |
| photo\_type    | TEXT    | Type d'image : PLAT, MENU, ou LIEU |
| photo\_chinois | TEXT    | "Chinois" ou "Non chinois"         |
| proba\_chinois | FLOAT   | Probabilité estimée par CLIP       |

---
## Resultat du Classification 

![proba](https://github.com/user-attachments/assets/534a463d-105a-4cd8-9c44-b23b8046d943)

## 🛠️ Technologies utilisées

* 📦 **Apify** – Scraping des données de restaurant
* 🌐 **Google Places API** – Collecte d’images
* 🗄️ **PostgreSQL** – Stockage structuré des données
* ☁️ **Railway** – Hébergement de la base PostgreSQL
* 🧠 **OpenAI CLIP** – Modèle de vision par ordinateur
* 📓 **Google Colab** – Environnement GPU pour exécution du pipeline
* 🐍 **Python + pandas + matplotlib** – Traitement & visualisation

---

## 🔮 Améliorations futures

* 📈 Entraîner un modèle spécialisé (finetuned CLIP ou CNN) pour les menus asiatiques.
* 🌍 Déploiement d’une interface Web (Streamlit, FastAPI ou Gradio).
* 🕵️‍♂️ Intégration d’un moteur de recherche visuelle pour restaurants similaires.
* 🔄 Automatisation complète via **n8n** ou Airflow.

---

## 🤝 Contribuer

Pull requests bienvenues ! Si vous avez des idées ou des améliorations, n'hésitez pas à les soumettre.
