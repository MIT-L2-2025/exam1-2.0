# Analyse de l'Authenticité des Restaurants à Antananarivo

Ce projet analyse l'authenticité de restaurants à Antananarivo (Madagascar), en se concentrant sur la cuisine asiatique (chinoise, vietnamienne, etc.). Il utilise un pipeline Python pour :
- Traiter des données de restaurants (nom, adresse, menu, avis, décor).
- Calculer des scores d’authenticité en pourcentage via un agent NLP (spaCy).
- Générer un graphe NetworkX représentant les relations entre nom, menu, avis, et décor.
- Produire un rapport PDF avec les résultats.

Le projet a été développé dans le cadre d’un travail académique (MITL2, Mai 2025) et est conçu pour analyser un nombre arbitraire de restaurants (n).

## Fonctionnalités
- **Entrée** : Fichier JSON (`restaurants.json`) avec nom, adresse, et photo des restaurants.
- **Pipeline** :
  - Ajout des colonnes `menu`, `reviews`, `decor` (manuellement ou via extrapolation).
  - Analyse NLP pour scorer l’authenticité (mots-clés : “chinois”, “dim sum”, “pho”, etc.).
  - Score global : 40% avis, 40% menu, 20% décor, exprimé en % (0-100).
  - Génération d’un graphe NetworkX (`graphe_scores_n.gml`).
  - Rapport PDF avec tableau des scores et visualisation du graphe.
- **Sortie** (exemple pour 9 restaurants) :
  - **La Muraille de Chine** : 56% (le plus authentique).
  - **Tanà Saïgon** : 44%.
  - **Restaurants Le Jasmin-Analakely** : 40%.
  - Restaurants non-asiatiques (ex. : La Jonquille) : 0%.

## Structure du Projet
```
├── restaurants.json            # Données d’entrée (9 restaurants)
├── restaurants_clean.csv       # Alternative CSV (optionnel)
├── create_restaurants_selected_n.py  # Crée restaurants_selected_n.csv avec menu/reviews/decor
├── restaurants_selected.py     # Sélectionne n restaurants asiatiques
├── analyze_restaurants_n.py    # Pipeline principal (scores, graphe, rapport)
├── restaurants_selected_n.csv  # Données avec menu/reviews/decor
├── restaurants_scored_n.csv   # Scores en %
├── graphe_scores_n.gml        # Graphe NetworkX
├── graphe_n.png               # Visualisation du graphe
├── rapport_authenticite_9.pdf # Rapport final
└── README.md                  # Ce fichier
```

## Pré-requis
- **Python** : 3.8+
- **Bibliothèques** :
  ```bash
  pip install pandas spacy networkx matplotlib reportlab
  python -m spacy download fr_core_news_sm
  ```
- **Système** : Testé sur Linux (Ubuntu). Chemins dans les scripts : `/home/manda/Téléchargements/MITL2/RESTAURANTS/`. Modifiez si nécessaire :
  ```python
  df = pd.read_csv("VOTRE_DOSSIER/restaurants_selected_n.csv")
  ```

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/VOTRE_UTILISATEUR/restaurants-authenticity.git
   cd restaurants-authenticity
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
   Créez `requirements.txt` avec :
   ```
   pandas
   spacy
   networkx
   matplotlib
   reportlab
   ```
3. Placez `restaurants.json` dans le dossier racine ou dans `/home/manda/Téléchargements/MITL2/RESTAURANTS/`.

## Utilisation
1. **Préparer les données** :
   - Exécutez `create_restaurants_selected_n.py` pour générer `restaurants_selected_n.csv` avec `menu`, `reviews`, `decor` pour les 9 restaurants :
     ```bash
     python create_restaurants_selected_n.py
     ```
   - Alternativement, utilisez `restaurants_selected.py` pour sélectionner n restaurants (ex. : restaurants asiatiques) :
     ```bash
     python restaurants_selected.py
     ```
     Modifiez `n` dans `restaurants_selected.py` si nécessaire :
     ```python
     n = 5  # Pour 5 restaurants
     ```
2. **Analyser l’authenticité** :
   - Exécutez `analyze_restaurants_n.py` pour calculer les scores, générer le graphe, et produire le rapport :
     ```bash
     python analyze_restaurants_n.py
     ```
3. **Vérifier les sorties** :
   - Scores : `restaurants_scored_n.csv`
   - Graphe : `graphe_scores_n.gml`, `graphe_n.png`
   - Rapport : `rapport_authenticite_9.pdf`

## Exemple de Sortie
```
Scores d’authenticité pour 9 restaurants (en %) :
                              name  score_reviews_pct  score_menu_pct  score_decor_pct  authenticity_score_pct
0     Le Grand Restaurant de Chine              60.0            20.0             20.0                   36.0
1  Restaurants Le Jasmin-Analakely              60.0            20.0             40.0                   40.0
2             La Muraille de Chine              80.0            40.0             40.0                   56.0
3                     La Jonquille               0.0             0.0              0.0                    0.0
4                      La Dynastie              20.0            20.0             20.0                   12.0
5                      Bon Appétit               0.0             0.0              0.0                    0.0
6               La Bastide Blanche               0.0             0.0              0.0                    0.0
7                      Tanà Saïgon              60.0            40.0             20.0                   44.0
8                        Le Muguet               0.0             0.0              0.0                    0.0
```

## Personnalisation
- **Données** :
  - Mettez à jour `menu`, `reviews`, `decor` dans `restaurants_selected_n.csv` avec des données réelles (ex. : Google Reviews) :
    ```python
    df = pd.read_csv("restaurants_selected_n.csv")
    df.loc[df["name"] == "La Dynastie", "menu"] = "nems, chow mein"
    df.to_csv("restaurants_selected_n.csv", index=False)
    ```
- **Mots-clés** :
  - Ajoutez des mots-clés dans `analyze_restaurants_n.py` pour améliorer les scores :
    ```python
    keywords.extend(["wok", "soja", "bambou"])
    ```
- **Poids des scores** :
  - Ajustez les pondérations dans `analyze_restaurants_n.py` :
    ```python
    df["authenticity_score_pct"] = (0.5 * df["score_reviews"] + 0.3 * df["score_menu"] + 0.2 * df["score_decor"]) * 20
    ```
- **Nombre de restaurants** :
  - Limitez à n restaurants (ex. : 5 asiatiques) dans `restaurants_selected.py` :
    ```python
    n = 5
    ```

## Notes
- **Données** : Les colonnes `menu`, `reviews`, `decor` sont partiellement extrapolées. Mettez à jour avec des données réelles pour de meilleurs scores.
- **Images** : La plupart des URLs photo sont des placeholders. Remplacez par des URLs réelles si disponibles.

## Contribuer
1. Forkez le dépôt.
2. Créez une branche (`git checkout -b feature/nouvelle-fonction`).
3. Commitez vos changements (`git commit -m "Ajout de fonctionnalité"`).
4. Poussez vers la branche (`git push origin feature/nouvelle-fonction`).
5. Ouvrez une Pull Request.

## Licence
Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## Contact
Pour toute question, contactez [VOTRE_EMAIL] ou ouvrez une issue sur GitHub.