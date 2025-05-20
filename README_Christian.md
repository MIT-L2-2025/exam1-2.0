# Detecteur de Restaurant à Antananarivo

Ce projet automatise la détection et la classification de restaurants chinois à Antananarivo, en trois grandes étapes : collecte, stockage et analyse.

---

## 1. Collecte des données (n8n)

1. **Source** :

   * **Apify** : extraction de restaurants potentiels (dataset Apify).
   * **Google Maps API** : récupération des détails (`name`, `address`, `coordinates`, `contact`) et jusqu’à 10 photos par restaurant.
2. **Détails récupérés** :

   * Nom du restaurant
   * Adresse postale
   * Coordonnées géographiques (latitude, longitude)
   * Contact (téléphone, site web le cas échéant)
   * URLs des images (0 à 10), non triées selon leur catégorie
3. **Types d’images** (non classées à ce stade) :

   * Photo de plat
   * Photo de menu
   * Photo des lieux du restaurant

---

## 2. Stockage des données (n8n)

1. **Images** :

   * Transfert des URLs Google vers **Cloudinary** pour limiter les appels API et optimiser la distribution.
2. **Base de données** :

   * **Supabase/PostgreSQL** : tables `restaurants` et `photos`.

| Table       | Colonnes principales                                             |
| ----------- | ---------------------------------------------------------------- |
| restaurants | id (PK), name, address, latitude, longitude, contact, ...        |
| photos      | id (PK), restaurant\_id (FK), url\_cloudinary, category (future) |

3. **Workflow** :

   * Séparation des flux « infos restaurant » et « photos » à l’aide de nœuds Code et If
   * Boucle par lots (`SplitInBatches`) pour insérer :

     * Les métadonnées du restaurant
     * Les photos associées

---

## 3. Analyse et classification (Kaggle / Python)

1. **Chargement** :

   * Extraction des tables `restaurants` et `photos` depuis Supabase
   * Conversion en `pandas.DataFrame`
2. **Classification des photos** :

   * Utilisation de **CLIP** pour assigner à chaque image une catégorie : plat, menu ou lieu
   * Calcul d’un score de « chinoisité » pour chaque photo
3. **Classification du nom** :

   * Application de **BERT** et d’expressions régulières (`re`) pour estimer la probabilité qu’un nom soit chinois
4. **Fusion des scores** :

   * Pondération des résultats (nom + photos) pour obtenir un score global de « Restaurant Chinois »
5. **Affichage** :

   * Génération d’un rapport HTML présentant pour chaque restaurant :

     * Score global
     * Scores détaillés par catégorie (nom, plat, menu, lieu)

---

## Prérequis

* **n8n** (>= 0.200.0)
* **Compte Apify** avec accès au dataset
* **Clé API Google Maps Places**
* **Compte Cloudinary** (cloud name, API key & secret)
* **Instance Supabase/PostgreSQL** avec tables `restaurants` et `photos`
* **Python 3.8+ sur Kaggle** avec les bibliothèques :

  * `pandas`, `requests`, `torch`, `transformers`, `clip` ou équivalent


HERIMANANTSOA Manitriniaina Christian



