import pandas as pd

DATA_PATH = "data/"

def obesity_prevalence_pre_processing(annee=2022):
    df = pd.read_csv(DATA_PATH + "obesity_prevalence_world.csv")

    df_annee = df[df["Year"]==annee].drop(columns="Year")

    # print(df.value_counts("Year"))

    return df_annee


def obesity_prevalence_pre_processing_without_year():
    df = pd.read_csv(DATA_PATH + "obesity_prevalence_world.csv")

    return df