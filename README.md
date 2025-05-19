# 🌟 Projet : Cartographie & Classification des Restaurants Chinois à Antananarivo

## 🎯 Objectif
__ Recueillir automatiquement les restaurants chinois situés à Antananarivo avec les informations suivantes :
   - Nom
   - Adresse
   - Latitude et longitude
   - Contact
   - Itinéraire (via Google Maps)
   - Carte interactive

__ Classer chaque restaurant selon son authenticité perçue en trois catégories :
   - Vraiment chinois 🥇
   - Moyennement chinois 🥈
   - Pas chinois 🥉

---

## 🛠️ Technologies Utilisées

__ **n8n (workflow automation)** :
   - Collecte des données (scraping automatisé)
   - Classification par score et règles heuristiques

__ **Langages de programmation** :
   - `Python` : création des graphes et calculs éventuels
   - `JavaScript` : exécution dans les nœuds Code de n8n + génération HTML

---

## 📁 Description des Fichiers

### 📄 Fichier 1 : `getData_wf.json`
- Workflow n8n qui effectue la **collecte automatique** des restaurants à partir de diverses sources en ligne.
- Génère automatiquement un fichier **restaurantDB.json** contenant les données brutes des restaurants chinois.

---

### 📄 Fichier 2 : `Recensement_wf.json`
- Workflow n8n responsable de la **recensement des restaurants**.
- Utilise les données extraites dans **restaurantDB.json**.
- Produit automatiquement le fichier **restaurants-db.html** (interface de résultat).

---

### 🌐 Fichier 3 : `restaurant-db.html`
- Page web interactive pour **visualiser les résultats** de la classification.

---

### Fichier 4 : 'Graphe Analytique/Analyse.py'
- Script python pour anlyser l'authenticité ou non des restaurants chinoix.

---

### Dossier 'Visualisation & 3D'

- Représentation sous forme 3D avec itinéraire et caractéristiques des restaurants.

---

Fonctionnalités :
- 💡 **Tableau des scores** avec affichage des critères de classement.
- 📊 **Diagramme** de répartition des types de restaurants.
- 🔍 **Recherche dynamique** d’un restaurant par nom.
- 📌 **Détails complets** d’un restaurant accessibles en un clic (via modale).
- 🗺️ **Carte et itinéraire** intégrés via Google Maps.

> 💾 Pour tester : ouvrez `restaurant-db.html` dans un navigateur moderne.

