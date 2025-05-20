import pandas as pd
# Charger CSV
df = pd.read_csv("restaurants_clean.csv")

# Sélectionner 2 restaurants
selected_restaurants = df[df["name"].str.contains("jasmin", case=False, na=False)].head(2)
if len(selected_restaurants) < 10:
    selected_restaurants = df.head(2)
print(selected_restaurants[["name", "address"]])
selected_restaurants.to_csv("restaurants_selected.csv", index=False)
