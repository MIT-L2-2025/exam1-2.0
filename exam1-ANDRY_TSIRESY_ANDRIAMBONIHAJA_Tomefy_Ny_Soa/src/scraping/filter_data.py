import json
import pandas as pd
import networkx as nx

with open("../restaurants.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def nettoyer_texte(texte):
    if texte is None:
        return ""
    if isinstance(texte, list):
        return " ".join(str(t).strip().lower() for t in texte)
    return str(texte).strip().lower()

for resto in data:
    resto["name_norm"] = nettoyer_texte(resto.get("name"))
    resto["address_norm"] = nettoyer_texte(resto.get("address"))
    resto["offerings_norm"] = nettoyer_texte(resto.get("offerings"))
    resto["highlights_norm"] = nettoyer_texte(resto.get("highlights"))
    resto["dining_options_norm"] = nettoyer_texte(resto.get("dining_options"))
    resto["atmosphere_norm"] = nettoyer_texte(resto.get("atmosphere"))


mots_cles = [
    "chinois", "chine", "beijing", "shanghai", "dim sum", "dumplings", "nouilles", "noodles",
    "peking", "szechuan", "canton", "ma po tofu", "char siu", "hot pot", "cha", "thé", "bao", "wonton",
    "sichuan", "hunan", "fujian", "guangdong", "cantonese", "mandarin"
]

for resto in data:
    contenu = " ".join([
        resto["name_norm"],
        resto["address_norm"],
        resto["offerings_norm"],
        resto["highlights_norm"],
        resto["dining_options_norm"],
        resto["atmosphere_norm"]
    ])
    mots_trouves = [mot for mot in mots_cles if mot in contenu]
    resto["matched_keywords"] = mots_trouves

G = nx.Graph()

for i, resto in enumerate(data):
    G.add_node(i, name=resto["name"], keywords=set(resto["matched_keywords"]))

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        k1 = G.nodes[i]["keywords"]
        k2 = G.nodes[j]["keywords"]
        communs = k1 & k2
        if communs:
            G.add_edge(i, j, weight=len(communs), shared_keywords=list(communs))


composantes = list(nx.connected_components(G))
groupes = {}
for id_groupe, composante in enumerate(composantes):
    for node in composante:
        groupes[node] = id_groupe


resultats = []
for i, resto in enumerate(data):
    resultats.append({
        "name": resto["name"],
        "matched_keywords": ", ".join(resto["matched_keywords"]),
        "cluster_id": groupes.get(i, -1)
    })

df = pd.DataFrame(resultats)
df = df.sort_values("cluster_id").reset_index(drop=True)

import ace_tools as tools; tools.display_dataframe_to_user(
    name="Clusters de Restaurants Chinois",
    dataframe=df
)
