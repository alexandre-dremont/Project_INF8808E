from banque_mondiale import load_banque_mondiale
from ncd import load_ncd_risk_complete
from dietary_compositions import dietary_compositions_pre_processing_total_without_year
from physical_activity import load_physical_activity

import pandas as pd

DATA_PATH = "data/"
RAW_DATA_PATH = "raw_data/"

def generate_correlation_matrix():
    df_gdp_ppp, df_health, df_gini = load_banque_mondiale()
    df_obesity = load_ncd_risk_complete()
    df_dietary = dietary_compositions_pre_processing_total_without_year()
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
    indicators = {
        'GDP_PPP': df_gdp_ppp,
        'Health_Expenditure': df_health,
        'Gini': df_gini
    }

    # other_indicators = {
    #     'Sedentary' : df_activity,
    #     'Calories': df_dietary
    # }

    corr_data = {}
    countries = df_obesity["ISO"].unique()

    for country_code in countries:

        if country_code in df_gdp_ppp["Country Code"].unique():
            df_obesity_country = df_obesity[df_obesity["ISO"] == country_code]\
                .drop(columns=["Country/Region/World", "ISO"])\
                .set_index("Year")[obesity_col]
            
            # print(country_code)
            # print(df_obesity_country)
            
            corr_data[country_code] = {}
            
            # Indicateurs Banque Mondiale
            for indicator, df_ind in indicators.items():
                unnamed_cols = [col for col in df_ind.columns if "Unnamed" in str(col)]

                df_ind_country = df_ind[df_ind["Country Code"] == country_code]\
                                    .drop(columns=["Country Name", "Country Code"] + unnamed_cols).T
                
                # print(df_ind_country)
                
                # print(indicator, df_ind_country.index)

                df_ind_country = df_ind_country.squeeze()
                df_ind_country = df_ind_country.replace("", float("nan")).astype("float")
                df_ind_country.index = df_ind_country.index.astype(int)

                # Aligner les séries sur les années communes
                common_years = df_obesity_country.index.intersection(df_ind_country.index)

                # print(country_code, common_years)
                # print(country_code, indicator, len(common_years))

                if len(common_years) < 2:
                    corr_data[country_code][indicator] = float("nan")
                    continue

                # corr_data[country_code][indicator] = df_ind_country.loc[common_years]\
                #     .corr(df_obesity_country.loc[common_years])

                corr_data[country_code][indicator] = safe_correlation(
                    df_ind_country.loc[common_years], 
                    df_obesity_country.loc[common_years]
                )
                
                # print(country_code, df_ind_country.loc[common_years].isna().sum())

            # Calories
            df_dietary_country = df_dietary[df_dietary["Code"] == country_code]\
                                    .set_index("Year")["Total"]

            common_years = df_obesity_country.index.intersection(df_dietary_country.index)

            if len(common_years) < 2:
                    corr_data[country_code]["Calories"] = float("nan")
            else:
                # corr_data[country_code]["Calories"] = df_dietary_country.loc[common_years]\
                #     .corr(df_obesity_country.loc[common_years])
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
                # corr_data[country_code]["Sedentary"] = df_activity_country.loc[common_years]\
                #     .corr(df_obesity_country.loc[common_years])

                corr_data[country_code]["Sedentary"] = safe_correlation(
                    df_activity_country.loc[common_years], 
                    df_obesity_country.loc[common_years]
                )
            
            # Exclure les pays sans donnée
            if any(pd.isna(v) for v in corr_data[country_code].values()):
                del corr_data[country_code]
       
    
    df_matrix = pd.DataFrame(corr_data)

    # print(df_matrix.shape)
    return df_matrix

def safe_correlation(s1, s2, min_points=2):
    combined = pd.concat([s1, s2], axis=1).dropna()
    if len(combined) < min_points:
        #  print(combined)
        return float("nan")
    return combined.iloc[:, 0].corr(combined.iloc[:, 1])

generate_correlation_matrix()