
---

## 🔁 Étapes du Workflow

1. **Recherche initiale**
   - 🔍 `HTTP Request` : `textsearch` API avec le mot-clé _restaurant chinois Antananarivo_

2. **Extraction & Pagination**
   - 📄 Extraction des données + récupération du `next_page_token` si disponible
   - ⏳ Ajout de `Wait` nodes pour respecter les délais de pagination
   - 🔁 Trois pages de résultats sont traitées, puis fusionnées

3. **Nettoyage & Enrichissement**
   - 🧹 Extraction des champs utiles (nom, adresse, géolocalisation, type, etc.)
   - 🔁 Boucle sur chaque restaurant (`SplitInBatches`)
   - 📲 Appel de l’API `place/details` pour enrichir les infos

4. **Analyse IA**
   - 🧠 Création d’un prompt structuré avec `Code` node (`Code8`)
   - ✨ Envoi du prompt vers OpenRouter (`OpenRouter Chat Model`)
   - 📊 Retour du score `"chinese_match_score"`

5. **Présentation & Export**
   - 🧾 Fusion des données brutes + réponse IA
   - 🖼️ Génération d’une page HTML (`Code10`)
   - 📦 Fichier encodé en base64 (prêt à télécharger)

---

## 📦 Fichier généré

Un fichier HTML encodé (nommé `restaurants_chinois_antananarivo.html`) est généré et téléchargeable depuis le workflow dans n8n.

---

## 🔐 Clés API nécessaires

Pour que le workflow fonctionne correctement, tu dois fournir :

- **Google Places API Key**  
  Requises pour accéder aux endpoints `textsearch` et `details`.

- **OpenRouter API Key**  
  Pour interagir avec un modèle d’IA et obtenir un score intelligent.

> 🔒 **⚠️ Assure-toi de ne pas exposer publiquement tes clés API.**

---

## 🛠️ Technologies utilisées

- [n8n](https://n8n.io) – Automation workflow
- [Google Maps Platform](https://developers.google.com/maps) – Recherche de lieux
- [OpenRouter](https://openrouter.ai) – Modèle IA conversationnel
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) – Traitement des données
- [HTML/CSS](https://developer.mozilla.org/fr/docs/Web/HTML) – Génération de la page finale

---

## 💡 Améliorations futures

- 📍 Filtrage dynamique par ville ou région
- 💬 Interface utilisateur pour choisir les types de cuisine
- 🔄 Cron trigger pour exécuter automatiquement


## 📝 Licence

Ce projet est sous licence MIT-MISA.  
Tu peux l’utiliser, le modifier et le distribuer librement en changeant les clé api utilisé.

---

## 🧪 Aperçu du HTML

```html
<h2>Le Dragon d'Or</h2>
<img src="https://maps.googleapis.com/maps/api/place/photo?photoreference=XXXXX" alt="Photo de Le Dragon d'Or">
<p><strong>Adresse :</strong> Rue XYZ, Antananarivo</p>
<p><strong>Score de correspondance chinoise :</strong> 85%</p>
...
