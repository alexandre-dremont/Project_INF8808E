import pandas as pd

DATA_PATH = "data/"
RAW_DATA_PATH = "raw_data/" # dossier uniquement disponible en local

mapping_countries_3 = {
    'Brunei' : 'Brunei Darussalam',
    'Cape Verde': 'Cabo Verde',
    'Democratic Republic of Congo': 'DR Congo',
    'Syria': 'Syrian Arab Republic',
    'Turkey': 'Turkiye',
    'Vietnam': 'Viet Nam',
    'Micronesia (FAO)': 'Federated States of Micronesia',
    'Russia': 'Russian Federation',
    'United States': 'United States of America',
    'Guinea-Bissau': 'Guinea Bissau',
    'Brunei': 'Brunei Darussalam',
    'Laos': 'Lao PDR',
    'Serbia and Montenegro': 'Serbia',
    'East Timor': 'Timor-Leste'
}

def reduce_dietary_compositions_dataset(rolling_window=5, sample=10):
    """Réduit les données provenant de la source Our World in Data.
    Utilise une fenêtre glissante de 5 ans et échantionne les données tous les 10 ans.
    Génère le fichier CSV "dietary-compositions-by-commodity-group-reduced.csv" stocké dans le dossier data.

    Args:
        rolling_window (int, optional): fenêtre glissante. Par défaut à 5 ans.
        sample (int, optional): nombre d'années pour l'échantillonnage. Par défaut à 10 ans.
    """
    df = pd.read_csv(RAW_DATA_PATH + "dietary-compositions-by-commodity-group.csv")

    non_numeric_cols = ["Entity", "Code", "Year"]
    countries = df["Entity"].unique()

    df["Total"] = df.iloc[:,2:].sum(axis=1)

    results = []

    for country in countries:
        df_country = df[df["Entity"]==country].sort_values("Year")

        df_lisse = df_country.drop(columns=non_numeric_cols).rolling(window=rolling_window, 
                        center=True, min_periods=1).mean()

        df_final = pd.concat([
            df_country[non_numeric_cols].reset_index(drop=True), 
            df_lisse.reset_index(drop=True)
        ], axis=1)
        df_final = df_final[df_final["Year"] % sample == 0]

        results.append(df_final)

    df_all = pd.concat(results, ignore_index=True)

    df_all.to_csv(DATA_PATH + "dietary-compositions-by-commodity-group-reduced.csv", index=False)

# reduce_dietary_compositions_dataset()


def load_data_dietary_compositions():
    """Charge les données donnant les apports caloriques quotidiens par pays (Our World in Data).
    Utilisée pour afficher le small multiples slope chart.

    Returns:
        dataframe: apports caloriques quotidiens par pays et par catégorie d'aliments
    """
    df = pd.read_csv(DATA_PATH + "dietary-compositions-by-commodity-group-reduced.csv")

    df.columns = ["Entity", "Code", "Year",
                "Autres", "Boissons alcoolisées", "Sucre", "Huiles et graisses", "Viande", "Produits laitiers et œufs",
                "Fruits et légumes", "Racines féculentes", "Légumineuses", "Céréales et grains", "Total"]
    
    df["Entity"] = df["Entity"].replace(mapping_countries_3)

    return df

def load_data_dietary_compositions_total():
    """Charge les données donnant les apports caloriques quotidiens par pays (Our World in Data).
    Ajoute une colonne correspondant au total des apports caloriques quotidiens.
    Utilisée pour afficher les corrélations entre la prévalence de l'obésité et le total des apports caloriques quotidiens par pays.

    Returns:
        dataframe: total des apports caloriques quotidiens par pays
    """
    df = pd.read_csv(DATA_PATH + "dietary-compositions-by-commodity-group-reduced.csv")
    df["Total"] = df.iloc[:,2:].sum(axis=1)

    df["Entity"] = df["Entity"].replace(mapping_countries_3)

    return df[["Entity", "Code", "Year", "Total"]]
