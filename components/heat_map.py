from data_preprocessing.banque_mondiale import banque_mondiale_pre_processing, load_banque_mondiale
from data_preprocessing.obesity_prevalence import obesity_prevalence_most_recent, obesity_prevalence_pre_processing_without_year
from data_preprocessing.ncd import load_ncd_risk, load_ncd_risk_complete
from data_preprocessing.dietary_compositions import dietary_compositions_pre_processing_total_without_year
from data_preprocessing.physical_activity import load_physical_activity
import pandas as pd
import plotly.express as px


def create_heat_map(nb_countries=10):
    df_gdp_ppp, df_health, df_gini = load_banque_mondiale()
    df_obesity = load_ncd_risk_complete()
    df_dietary = dietary_compositions_pre_processing_total_without_year()
    df_activity = load_physical_activity

    # df_obesity = obesity_prevalence_pre_processing_without_year()

    # df_obesity = obesity_prevalence_most_recent(df_obesity)

    # df = df_indicator.merge(df_obesity, left_on="Country Name", right_on="Country")

    # print(df.head())

    # Indicateurs
    indicators = ["GDP_PPP", "Health_Expenditure", "Gini"]

    obesity_col = "Prevalence of BMI>=30 kg/m² (obesity)"

    df_matrix = correlation_matrix(df_obesity, df_gdp_ppp, df_health, df_gini, df_activity, df_dietary, obesity_col, nb_countries)

    fig = px.imshow(
        df_matrix, 
        labels=dict(x="Pays", y="Indicateur", color="Corrélation"), 
        color_continuous_scale="RdBu",
        range_color=[-1, 1],
        aspect="auto"
    )

    # Info-bulle
    fig.update_traces(hovertemplate=hover_template())

    return fig

def correlation_matrix(df_obesity, df_gdp_ppp, df_health, df_gini, df_activity, df_dietary, obesity_col, nb_countries):
    indicators = {
        'GDP_PPP': df_gdp_ppp,
        'Health_Expenditure': df_health,
        'Gini': df_gini
    }

    other_indicators = {
        'Sedentary' : df_activity,
        'Calories': df_dietary
    }

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

                corr_data[country_code][indicator] = df_ind_country.loc[common_years]\
                    .corr(df_obesity_country.loc[common_years])
                
                # print(country_code, df_ind_country.loc[common_years].isna().sum())
            
            # Exclure les pays sans donnée
            if any(pd.isna(v) for v in corr_data[country_code].values()):
                del corr_data[country_code]
       
    
    df_matrix = pd.DataFrame(corr_data)
    # print(df_matrix.iloc[:,:nb_countries])
    return df_matrix.iloc[:,:nb_countries]

# def correlation_matrix(df_obesity, df_gdp_ppp, df_health, df_gini, obesity_col):
#     corr_data = {}
#     countries = df_obesity["ISO"].unique()
#     for country_code in countries:
#         # print(country_code)
#         df_obesity_country = df_obesity[df_obesity["ISO"] == country_code].drop(columns=["Country/Region/World", "ISO"]).set_index("Year")[obesity_col]
#         df_gdp_ppp_country = df_gdp_ppp[df_gdp_ppp["Country Code"] == country_code].drop(columns=["Country Name", "Country Code"]).T
#         df_health_country = df_health[df_health["Country Code"] == country_code].drop(columns=["Country Name", "Country Code"]).T
#         df_gini_country = df_gini[df_gini["Country Code"] == country_code].drop(columns=["Country Name", "Country Code"]).T

#         print(df_obesity_country)
#         print(df_gdp_ppp_country)
#         corr_data[country_code] = {
#             'GDP_PPP': df_gdp_ppp_country.corr(df_obesity_country),
#             'Health_Expenditure': df_health_country.corr(df_obesity_country),
#             'Gini': df_gini_country.corr(df_obesity_country)
#         }
    
#     df_matrix = pd.DataFrame(corr_data)
#     return df_matrix


def hover_template():
    return (
        '<b>%{x}</b>'
        "<br>Indicateur : %{y}"
        "<br>Corrélation : %{z}"
        '<extra></extra>'
    )