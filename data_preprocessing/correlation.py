from banque_mondiale import load_banque_mondiale
from ncd import load_ncd_risk_complete
from dietary_compositions import load_data_dietary_compositions_total
from physical_activity import load_physical_activity

import pandas as pd

DATA_PATH = "data/"
RAW_DATA_PATH = "raw_data/"

def generate_correlation_matrix():
    """Charge les données provenant de NCD Risc
    Enregistre la matrice de corrélation dans un fichier CSV cette matrice pour éviter des calculs redondants.
    """
    df_gdp_ppp, df_health, df_gini = load_banque_mondiale()
    df_obesity = load_ncd_risk_complete()
    df_dietary = load_data_dietary_compositions_total()
    df_activity = load_physical_activity()

    obesity_col = "Prevalence of BMI>=30 kg/m² (obesity)"

    df_matrix = correlation_matrix(df_obesity, df_gdp_ppp, df_health, df_gini, df_activity, df_dietary, obesity_col)

    # Remplacer les codes ISO par les noms des pays 
    iso_to_country = df_obesity.set_index("ISO")["Country/Region/World"].to_dict()
    # Renommer les colonnes de la matrice
    df_matrix.columns = [iso_to_country.get(code, code) for code in df_matrix.columns]

    # Sauvegarder en format csv
    df_matrix.to_csv(DATA_PATH + "correlation_matrix.csv")


def correlation_matrix(df_obesity, df_gdp_ppp, df_health, df_gini, df_activity, df_dietary, obesity_col):
    """Génère une matrice de corrélation entre la prévalence de l'obésité et différents indicateurs socio-économiques
    (indice de Gini, sédentarité...). Les lignes correspondent aux indicateurs étudiés et les lignes aux pays.

    Args:
        df_obesity (dataframe): prévalence de l'obésité (NCD Risc)
        df_gdp_ppp (dataframe): PIB par habitant en parité de pouvoir d'achat (Banque Mondiale)
        df_health (dataframe): Dépenses de santé par habitant (Banque Mondiale)
        df_gini (dataframe): Indice de Gini (Banque Mondiale)
        df_activity (dataframe): Prévalence du manque d'activité physique (Organisation mondiale de la Santé)
        df_dietary (dataframe): Apports caloriques quotidiens (Our World in Data)
        obesity_col (dataframe): colonne cible pour la corrélation (prévalence de l'obésité)

    Returns:
        dataframe: matrice de corrélation
    """

    indicators = {
        'GDP_PPP': df_gdp_ppp,
        'Health_Expenditure': df_health,
        'Gini': df_gini
    }

    corr_data = {}

    # On récupère la liste des pays
    countries = df_obesity["ISO"].unique()

    for country_code in countries:

        if country_code in df_gdp_ppp["Country Code"].unique():
            df_obesity_country = df_obesity[df_obesity["ISO"] == country_code]\
                .drop(columns=["Country/Region/World", "ISO"])\
                .set_index("Year")[obesity_col]
            
            corr_data[country_code] = {}
            
            # Indicateurs Banque Mondiale
            for indicator, df_ind in indicators.items():
                unnamed_cols = [col for col in df_ind.columns if "Unnamed" in str(col)]

                df_ind_country = df_ind[df_ind["Country Code"] == country_code]\
                                    .drop(columns=["Country Name", "Country Code"] + unnamed_cols).T
               

                df_ind_country = df_ind_country.squeeze()
                df_ind_country = df_ind_country.replace("", float("nan")).astype("float")
                df_ind_country.index = df_ind_country.index.astype(int)

                # Aligner les séries sur les années communes
                common_years = df_obesity_country.index.intersection(df_ind_country.index)

                if len(common_years) < 2:
                    corr_data[country_code][indicator] = float("nan")
                    continue

                corr_data[country_code][indicator] = safe_correlation(
                    df_ind_country.loc[common_years], 
                    df_obesity_country.loc[common_years]
                )

            # Calories
            df_dietary_country = df_dietary[df_dietary["Code"] == country_code]\
                                    .set_index("Year")["Total"]

            common_years = df_obesity_country.index.intersection(df_dietary_country.index)

            if len(common_years) < 2:
                    corr_data[country_code]["Calories"] = float("nan")
            else:
                corr_data[country_code]["Calories"] = safe_correlation(
                    df_dietary_country.loc[common_years], 
                    df_obesity_country.loc[common_years]
                )
                
            # Sédentarité
            # On récupère les noms de pays correspondant aux codes ISO
            country_name = df_obesity[df_obesity["ISO"] == country_code]["Country/Region/World"].iloc[0]

            df_activity_country = df_activity[df_activity["Location"] == country_name]\
                                    .set_index("Period")["Both_sexes_val"]

            common_years = df_obesity_country.index.intersection(df_activity_country.index)

            if len(common_years) < 2:
                    corr_data[country_code]["Sedentary"] = float("nan")
            else:

                corr_data[country_code]["Sedentary"] = safe_correlation(
                    df_activity_country.loc[common_years], 
                    df_obesity_country.loc[common_years]
                )
            
            # Exclure les pays sans donnée
            if any(pd.isna(v) for v in corr_data[country_code].values()):
                del corr_data[country_code]
       
    
    df_matrix = pd.DataFrame(corr_data)

    return df_matrix

def safe_correlation(s1, s2, min_points=2):
    """Calcul la corrélation de Pearson entre deux séries. Si les colonnes ne comportent pas au moins min_points données,
    la corrélation vaut "nan"

    Args:
        s1 (Serie): 1ère colonne
        s2 (Serie): 2ème colonne
        min_points (int, optional): nombre minimal de données pour calcul la corrélation. Par défaut à 2.

    Returns:
        Serie: corrélation
    """
    combined = pd.concat([s1, s2], axis=1).dropna()
    if len(combined) < min_points:
        #  print(combined)
        return float("nan")
    return combined.iloc[:, 0].corr(combined.iloc[:, 1])

# generate_correlation_matrix()