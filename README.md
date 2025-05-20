# 🍜 Recensement des Restaurants Chinois à Antananarivo avec n8n

Ce projet vise à recenser les restaurants chinois présents à Antananarivo (Madagascar) en utilisant une automatisation réalisée avec n8n . Un test statistique de khi-deux (χ²) est appliqué pour évaluer la probabilité qu’un établissement soit réellement un restaurant chinois, et les résultats sont affichés dans une interface HTML conviviale.

## 🧰 Technologies Utilisées

**n8n** : Orchestrateur d'automatisations
**JavaScript/TypeScript** : Scripts personnalisés dans n8n
**HTML/CSS** : Interface utilisateur pour visualiser les résultats
**Statistiques (Khi-2)** : Analyse probabiliste pour valider les données

## 📌 Objectif du Projet

L’objectif principal est de collecter des informations sur les restaurants se présentant comme chinois à Antananarivo, puis d’évaluer la fiabilité de cette classification via un test statistique. Ce projet peut servir de base à une analyse plus poussée sur la représentation des cuisines asiatiques à Madagascar.

## 🧪 Méthodologie

** Collecte des Données : **
Extraction d'informations via des APIs ou web scraping automatisé avec n8n.
Filtre basé sur des mots-clés comme "chinois", "asiatique", etc.
** Test Statistique (Khi-2) : **
Comparaison des fréquences observées vs attendues pour valider si la classification comme "restaurant chinois" est statistiquement plausible.
Calcul de p-value pour chaque établissement.
** Visualisation : **
Résultats affichés dans une page HTML simple avec carte interactive et tableau de données.

## 📊 Résultats Clés

Le test du Khi-2 permet d’éviter les erreurs de classification. En général, un seuil de **p-value < 0.05** est utilisé pour considérer qu’un établissement ressemble statistiquement à un restaurant chinois.

