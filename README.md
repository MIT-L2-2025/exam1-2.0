# exam1-2.0
nouvelle version de l'examen précédent

# 🇨🇳 Chinese Restaurant with Probability - n8n Workflow

Ce projet est un **workflow automatisé sous n8n** permettant d’analyser des restaurants situés à Antananarivo pour estimer la probabilité qu’ils soient **des restaurants chinois**, en se basant sur :

- Des **informations textuelles extraites automatiquement**,
- L’analyse d’un **modèle de langage (LLM)**,
- Une combinaison de scores avec **pondération et ajustement statistique par khi²**.

---

## 🧠 Objectif

L'objectif du projet est de créer une **solution semi-automatique** qui :

1. Scrape des données de restaurants depuis un site web local (FindGlocals).
2. Extrait et nettoie les informations : nom, spécialités, adresse, image, lien, numéro de téléphone.
3. Utilise un **LLM (modèle de langage)** pour attribuer des probabilités :
   - Basées sur le **nom**,
   - Basées sur les **spécialités culinaires**.
4. Calcule un score final combiné, en ajustant selon un indicateur inspiré du **test khi²**, pour renforcer ou atténuer la confiance.

---

## 🔧 Fonctionnement du Workflow

Le workflow est divisé en plusieurs étapes :

### 1. Scraping & Extraction HTML

- 📍 **Source :** https://www.findglocal.com/MG/Antananarivo/
- 🧾 Données extraites :
  - `.inneritembox` → nom, adresse, spécialité, image, lien.
- 📸 Les images et liens sont également collectés.

### 2. Transformation JSON

- Les données HTML sont converties en objets JSON, où chaque restaurant est représenté comme une entrée propre.

### 3. Appels aux modèles LLM

- Un **prompt dynamique** est généré pour chaque restaurant.
- Deux types de prompts :
  - Version longue avec **justification** (analyse complète),
  - Version simple (nom + spécialités).
- Les modèles répondent en JSON au format :

```json
{
  "proba_nom": 85,
  "proba_specialite": 92,
  "justification": "Le nom contient 'Wang', commun dans les enseignes chinoises..."
}
