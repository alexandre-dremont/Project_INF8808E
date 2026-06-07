import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = "data/"

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



