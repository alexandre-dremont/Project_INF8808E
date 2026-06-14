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

def banque_mondiale_pre_processing(annee=2022, scale=True):
    gdp = pd.read_csv(DATA_PATH + "API_NY.GDP.PCAP.CD_DS2_en_csv_v2_121663.csv", skiprows=4, index_col="Country Name")
    gdp_ppp = pd.read_csv(DATA_PATH + "API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_121708.csv", skiprows=4, index_col="Country Name")
    health = pd.read_csv(DATA_PATH + "API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_645.csv", skiprows=4, index_col="Country Name")
    gini = pd.read_csv(DATA_PATH + "API_SI.POV.GINI_DS2_en_csv_v2_115456.csv", skiprows=4, index_col="Country Name")

    # print(gdp_ppp.isna().sum())

    df = pd.DataFrame(
        data={
            # "GDP":gdp[str(annee)],
            "GDP_PPP": gdp_ppp[str(annee)],
            "Health_Expenditure" : health[str(annee)],
            "Gini" : gini[str(annee)]
        },
        index=gdp_ppp.index
    )

    if not scale :
        return df

    scaler = MinMaxScaler()
    df_norm = pd.DataFrame(
        scaler.fit_transform(df),
        columns=df.columns
    )

    df_norm["Entity"]=df.index

    return df_norm

# print(banque_mondiale_pre_processing())

def load_banque_mondiale():
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



