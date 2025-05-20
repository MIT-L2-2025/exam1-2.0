# Examen 1 – Version 2.0

## Présentation

Ce dépôt présente la version 2.0 du projet d’examen, qui consiste à recenser les restaurants chinois situés à Antananarivo. Cette version améliore la précédente en apportant des correctifs, une meilleure organisation, et un enrichissement des données.

## Fonctionnalités

- 📍 Recensement automatique des restaurants chinois à Antananarivo via Overpass API
- 🗺️ Génération d’un fichier HTML (`restaurants.html`) affichant la liste des restaurants
- 🔄 Workflow n8n disponible (`resto_chinois_wf.json`) pour automatiser le processus
- ✅ Données au format JSON prêtes à être réutilisées
- 🧼 Amélioration de la structure et du nommage des fichiers par rapport à la version précédente

## Fichiers inclus

- `restaurants.html` : Affichage des restaurants chinois dans une page HTML lisible
- `resto_chinois_wf.json` : Fichier de workflow n8n pour automatiser l’extraction des données

## Comparaison avec la version précédente

| Élément                  | Version 1.0 ([exam1](https://github.com/MIT-L2-2025/exam1/tree/ANDRIMALALA-Isma%C3%ABl)) | Version 2.0 ([exam1-2.0](https://github.com/MIT-L2-2025/exam1-2.0/tree/ANDRIMALALA_Isma%C3%ABl)) |
|--------------------------|--------------------------------------------------------|------------------------------------------------------------|
| **Nom du fichier JSON**  | `restos-chinois.json`                                  | `resto_chinois_wf.json`                                    |
| **Affichage HTML**       | Basique                                                | Structuré et amélioré                                      |
| **Automatisation n8n**   | Présente                                               | Améliorée (workflow mieux structuré)                       |
| **Structure du projet**  | Simple                                                 | Plus claire et organisée                                   |
| **But principal**        | Extraire et afficher des restaurants chinois           | Optimiser et rendre plus maintenable le projet initial     |

## Instructions d’utilisation

1. Ouvrez `restaurants.html` dans un navigateur pour consulter la liste des restaurants chinois.
2. Importez le fichier `resto_chinois_wf.json` dans n8n pour examiner ou exécuter le workflow.
3. Vous pouvez adapter le workflow pour mettre à jour les données automatiquement.

## Remarque

Omission du vue 360° avec pegman dans cette version à cause des limites posés par les api.

## Auteur

ANDRIMALALA Ismaël

---
