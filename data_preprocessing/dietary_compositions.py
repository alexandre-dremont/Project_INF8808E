import pandas as pd

DATA_PATH = "data/"

def dietary_compositions_pre_processing_total(annee=2019):
    df = pd.read_csv(DATA_PATH + "dietary-compositions-by-commodity-group.csv")
    df_annee = df[df["Year"]==annee][["Entity", "Code"]]
    df_annee["Total"] = df.iloc[:,2:].sum(axis=1)

    df_annee["Total"] = (df_annee["Total"]-df_annee["Total"].min())/(df_annee["Total"].max()-df_annee["Total"].min())

    return df_annee

# print(dietary_compositions_pre_processing_total())

def dietary_compositions_pre_processing():
    df = pd.read_csv(DATA_PATH + "dietary-compositions-by-commodity-group.csv")

    return df

# print(dietary_compositions_pre_processing().columns)