import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = "data/"

mapping_countries = {
    "Bahamas, The": "Bahamas",
    "Congo, Dem. Rep.": "DR Congo",
    "Congo, Rep.": "Congo",
    "Egypt, Arab Rep.": "Egypt",
    "Gambia, The": "Gambia",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Micronesia, Fed. Sts.": "Federated States of Micronesia",
    "Iran, Islamic Rep.": "Iran",
    "Korea, Dem. People's Rep.": "North Korea",
    "Korea, Rep.": "South Korea",
    "Slovak Republic": "Slovakia",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Lucia": "Saint Lucia",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Venezuela, RB": "Venezuela",
    "West Bank and Gaza": "Palestine",
    "Yemen, Rep.": "Yemen",
    "United States": "United States of America",
    "Puerto Rico (US)": "Puerto Rico",
    "Guinea-Bissau": "Guinea Bissau",
    "Somalia, Fed. Rep.": "Somalia"
}

def load_banque_mondiale():
    """Charge les données provenant de la banque mondiale, 
    applique une uniformisation des noms des pays avec le dictionnaire mapping_countries

    Returns:
        dataframe, dataframe, dataframe: 3 dataframes contenant respectivement les indicateurs : PIB PPA, dépenses de santé par habitant et indice de Gini
    """
    # gdp = pd.read_csv(DATA_PATH + "API_NY.GDP.PCAP.CD_DS2_en_csv_v2_121663.csv", skiprows=4)
    gdp_ppp = pd.read_csv(DATA_PATH + "API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_121708.csv", skiprows=4)
    health = pd.read_csv(DATA_PATH + "API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_645.csv", skiprows=4)
    gini = pd.read_csv(DATA_PATH + "API_SI.POV.GINI_DS2_en_csv_v2_115456.csv", skiprows=4)

    # print(gdp_ppp.isna().sum())

    # gdp = gdp.drop(columns=["Indicator Name","Indicator Code"])
    gdp_ppp = gdp_ppp.drop(columns=["Indicator Name","Indicator Code"])
    health = health.drop(columns=["Indicator Name","Indicator Code"])
    gini = gini.drop(columns=["Indicator Name","Indicator Code"])

    gdp_ppp["Country Name"] = gdp_ppp["Country Name"].replace(mapping_countries)
    health["Country Name"] = health["Country Name"].replace(mapping_countries)
    gini["Country Name"] = gini["Country Name"].replace(mapping_countries)

    return gdp_ppp, health, gini

# print(load_banque_mondiale())

def reduce_dataset_banque_mondiale(rolling_window=5, years=range(1980, 2030, 10)):
    """Agrège et réduit les données provenant de la banque mondiale (PIB PPA, dépenses de santé par habitant et indice de Gini).
    Utilise une fenêtre glissante de 5 ans et échantionne les données tous les 10 ans.
    Génère le fichier CSV "banque_mondiale-reduced.csv" stocké dans le dossier data.

    Args:
        rolling_window (int, optional): fenêtre glissante. Par défaut à 5 ans.
        years (_type_, optional): dates conservées. Par défaut à range(1980, 2030, 10).
    """
    df_gdp_ppp, df_health, df_gini = load_banque_mondiale()

    datasets = {
        "GDP_PPP": df_gdp_ppp,
        "Health_Expenditure": df_health,
        "Gini": df_gini
    }
    
    non_numeric_cols = ["Country Name", "Country Code"]
    year_cols = [col for col in df_gdp_ppp.columns if col not in non_numeric_cols and "Unnamed" not in str(col)]

    results = []

    for indicator_name, df in datasets.items():
        # Nettoyage des colonnes
        unnamed_cols = [col for col in df.columns if "Unnamed" in str(col)]
        df = df.drop(columns=unnamed_cols)

        for _, row in df.iterrows():
            country_name = row["Country Name"]
            country_code = row["Country Code"]

            # On extrait la série temporelle
            serie = row[year_cols].replace("", float("nan")).astype("float")
            serie.index = [int(y) for y in year_cols]

            # Lissage
            serie_lisse = serie.rolling(window=rolling_window, center=True, min_periods=1).mean()

            # Filtrage sur les années cibles
            for year in years:
                if year in serie_lisse.index:
                    results.append({
                        "Country Name": country_name,
                        "Country Code": country_code,
                        "Year": year,
                        indicator_name: serie_lisse[year]
                    })
        
    # Assembler et pivoter pour avoir les 3 indicateurs en colonnes
    df_long = pd.DataFrame(results)

    df_final = df_long.groupby(non_numeric_cols + ["Year"])\
                        .first()\
                        .reset_index()
    df_final.to_csv(DATA_PATH + "banque_mondiale-reduced.csv", index=False)

# reduce_dataset_banque_mondiale()

def load_reduced_banque_mondiale():
    """Charge le fichier CSV des données provenant de la banque mondiale (PIB PPA, dépenses de santé par habitant et indice de Gini),
    réduits avec la fonction reduce_dataset_banque_mondiale
    

    Returns:
        dataframe: données réduites et aggrégées de la banque mondiale
    """
    df = pd.read_csv(DATA_PATH + "banque_mondiale-reduced.csv")

    return df

