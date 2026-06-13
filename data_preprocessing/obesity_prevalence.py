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


def obesity_prevalence_most_recent(df):
    """Une ligne par pays avec l'enquête nationale la plus récente, revenu manquant étiqueté."""
    national = (df[df["Area"] == "National"]
                .sort_values("Year", ascending=False)
                .drop_duplicates(subset="Country", keep="first")
                .copy())
    # ~20 territoires absents de la classification de la Banque Mondiale
    national["Income_group"] = national["Income_group"].fillna("Non classé")
    return national.reset_index(drop=True)