# 🍜 Liste des Restaurants Chinois à Tananarive (n8n Workflow)

Ce projet est un **workflow n8n** qui permet de récupérer automatiquement une liste de restaurants chinois à Antananarivo (Madagascar), d’analyser leur pertinence, et de générer une page HTML riche et interactive contenant :

- Le nom du restaurant
- Sa photo, son adresse, téléphone et horaires
- Sa spécialité
- Un indice de "pertinence chinoise" basé sur un score statistique
- Une carte intégrée (Google Maps)
- Des liens vers son site et son itinéraire

---

## ⚙️ Fonctionnement du workflow

1. **Déclencheur manuel**
   - L'utilisateur clique sur « Test workflow » pour lancer le processus.

2. **Requête HTTP à l'API SerpAPI**
   - Récupération des résultats Google Maps avec les mots-clés `restaurant chinois antananarivo`.

3. **Traitement des données**
   - Calcul d’un indice de pertinence basé sur les mots-clés chinois dans les descriptions.
   - Génération d’un tableau JSON enrichi avec les coordonnées GPS, horaires, site web, etc.

4. **Génération HTML**
   - Création d’un fichier HTML animé et stylisé (responsive, avec cartes Google Maps intégrées).
   - Le fichier est exporté en local dans `restos-chinois.html`.

---

## 📁 Fichier de sortie

Le fichier HTML généré :  
📄 `restos-chinois.html`

Tu peux l'ouvrir dans ton navigateur pour voir le résultat.

---

## 🧪 Technologies utilisées

- [n8n](https://n8n.io) – automatisation des workflows
- [SerpAPI](https://serpapi.com/) – récupération des données Google Maps
- HTML/CSS (responsive + animations)
- JavaScript (analyse de texte, génération dynamique)
- Google Maps (iframe & liens)

---

## 📸 Aperçu du rendu

- Image du restaurant
- Coordonnées GPS
- Carte satellite interactive
- Lien direct vers l’itinéraire
- Indice de "chinois" (score de pertinence)

---

## 🔐 Configuration requise

- Une clé API **SerpAPI**
- n8n auto-hébergé (ou n8n Cloud)
- Droits d’écriture sur le disque pour sauvegarder le fichier `.html`

---

## 🛠 Personnalisation

Tu peux modifier :

- La **liste des mots-clés chinois** dans le node "Code"
- Le **design HTML** dans le node "Code1"
- Le **fichier de sortie** dans le node "Read/Write Files from Disk"

---

## 📦 Exemple de node principal (Code JS)

```javascript
const motsChinois = ["chinois", "baguette", "wok", "dim sum", "tsa-tsiou", ...];
function compterMots(text) { ... }
...
const pertinence_chinoise = Math.min(100, Math.round(chi2 * 10));
