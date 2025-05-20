Explication du principe de mon code:
-clé utilisé: clé API de Apify 
-les variables que j'ai definis : avis des clients,nom des restaurant,menu des restaurants,spécialité du restaurants
-les réponses du resultats sont générées dans le fichier html
-pour l'executer on a besoin d'installer les dépendances suivantes en executant la commande : pip install apify-client requests
-on doit aussi installer python3

Explication du focntionnement de mon code:
2. Recherche des restaurants (search_restaurants())
Principe : Envoie une requête à l'actor compass~crawler-google-places pour récupérer des données sur les restaurants à Antananarivo.

3. Filtrage par localisation (is_in_antananarivo())
Principe : Vérifie si un restaurant est à Antananarivo en recherchant « antananarivo » ou « madagascar » dans son adresse.
Sortie : Booléen (True si à Antananarivo, False sinon).

4. Évaluation des restaurants (check_chinese_indicators())
Principe : Calcule un score de pertinence pour chaque restaurant en fonction de cinq variables indiquant une cuisine chinoise.
Variables et scores :
Avis (35 %) : Détecte des avis positifs (ex. : « bonne », « délicieux ») mentionnant « chinois », « chinese », ou « cuisine chinoise » dans la description ou les avis.
Cuisine (25 %) : Identifie des termes comme « chinese », « nems », « riz cantonais » dans la description, les catégories ou les avis.
Menu (25 %, -2 % par plat non chinois) : Vérifie la présence de plats chinois (ex. : « nems », « canard laqué ») dans la description, avis, catégories ou menu. Pénalité de -2 % par plat non chinois unique (ex. : « pizza », « burger »).
Nom (10 %) : Recherche des noms suggestifs (ex. : « chine », « dragon », « muraille »).
Spécialité (20 %) : Détecte des plats chinois mis en avant dans la description ou les catégories.

5. Sélection et traitement des restaurants (main())
Principe : Filtre les restaurants selon leur localisation et leur score, puis construit une liste de dictionnaires pour l’affichage.

7. Génération du résultat HTML (generate_html())
Principe : Crée un fichier HTML (restaurants_chinois_antananarivo.html) avec un tableau des restaurants sélectionnés.

