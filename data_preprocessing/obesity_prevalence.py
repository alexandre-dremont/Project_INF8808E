import pandas as pd

DATA_PATH = "data/"

def load_income_group():
    """Charge les données de prévalence de l'obésité dans le monde (World Obesity Federation) et 
    renvoie uniquement les colonnes "Country" et "Income_group"

    Returns:
        dataframe: dataframe permettant de faire la correspondance entre les pays et les groupes de richesse
    """
    df = pd.read_csv(DATA_PATH + "obesity_prevalence_world.csv")

    return df[["Country", "Income_group"]]


def obesity_prevalence_most_recent(df):
    """Une ligne par pays avec l'enquête nationale la plus récente, revenu manquant étiqueté."""
    national = (df[df["Area"] == "National"]
                .sort_values("Year", ascending=False)
                .drop_duplicates(subset="Country", keep="first")
                .copy())
    # Environ 20 territoires absents de la classification de la Banque Mondiale
    national["Income_group"] = national["Income_group"].fillna("Non classé")
    return national.reset_index(drop=True)