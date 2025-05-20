

**Description**

Ce dépôt présente un workflow n8n conçu pour collecter, filtrer et générer une page HTML listant des restaurants chinois à Antananarivo à partir d'une API Apify.

---

### 🗂️ Table des matières

1. [Prérequis](#-prérequis)
2. [Structure du workflow](#-structure-du-workflow)
3. [Description des nœuds](#-description-des-nœuds)
4. [Exécution](#-exécution)
---

## 🔧 Prérequis

* Node.js (v14 ou supérieur)
* n8n installé globalement (`npm install -g n8n`)
* Clé API Apify valide (si nécessaire)

---

## 📊 Structure du workflow

Le workflow se compose de 5 nœuds principaux et 3 notes explicatives :

```
[ManualTrigger] → [HTTP Request] → [Extract result 2] → [Filtrer data] → [Code]
```

* **When clicking ‘Test workflow’** (*Manual Trigger*) : point d'entrée pour lancer le workflow à la demande.
* **Request with api.apify.com** (*HTTP Request*) : récupération au format JSON des données de restaurants depuis Apify.
* **Extract result 2** (*Code*) : extraction et normalisation des champs utiles (nom, coordonnées, adresse, contact, image, etc.).
* **Filtrer data** (*Code*) : filtrage des items pour ne conserver que les restaurants chinois avec une note ≥ 4.
* **Code** (*Code*) : génération d'un fichier HTML `restaurants_chinois.html` listant les restaurants formatés.
* **Sticky Notes** : explications visuelles intégrées au canvas n8n.

---

## 🔍 Description des nœuds

| Nœud                          | Type                | Description                                                                            |
| ----------------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| When clicking ‘Test workflow’ | Manual Trigger (v1) | Déclenchement manuel du workflow.                                                      |
| Request with api.apify.com    | HTTP Request (v4.2) | Appel GET vers l'API Apify pour récupérer des données JSON.                            |
| Extract result 2              | Code (JS)           | Transformation des données brutes en objet JSON structuré (nom, lat, lon, etc.).       |
| Filtrer data                  | Code (JS)           | Filtre les restaurants contenant le mot "chinois" (ou dérivés) et ayant une note ≥ 4.  |
| Code                          | Code (JS)           | Construit dynamiquement le HTML final et l’exporte en base64 pour création de fichier. |

---

## ▶️ Exécution

1. Dans l'interface n8n, importez le fichier JSON du workflow (`.json` fourni).
2. Cliquez sur **Test workflow** pour déclencher manuellement.
3. Vérifiez la sortie du nœud **Code** : un fichier `restaurants_chinois.html` sera généré.
4. Téléchargez et ouvrez ce fichier dans votre navigateur.

---
