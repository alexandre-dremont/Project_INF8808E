import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = "data/"

mapping_countries_2 = {
    "Bahamas": "Bahamas",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Democratic People's Republic of Korea": "North Korea",
    "Democratic Republic of the Congo": "DR Congo",
    "Guinea-Bissau": "Guinea Bissau",
    "Iran (Islamic Republic of)": "Iran",
    "Lao People's Democratic Republic": "Lao PDR",
    "Micronesia (Federated States of)": "Federated States of Micronesia",
    "Netherlands (Kingdom of the)": "Netherlands",
    "occupied Palestinian territory, including east Jerusalem": "Palestine",
    "Republic of Korea": "South Korea",
    "Republic of Moldova": "Moldova",
    "Türkiye": "Turkiye",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "United Republic of Tanzania": "Tanzania",
    "Venezuela (Bolivarian Republic of)": "Venezuela"
}

def load_physical_activity():
    """Charge les données permettant d'analyser la sédentarité dans le monde (Organisation Mondiale de la Santé)
    Utilisée pour afficher les corrélations entre la prévalence de l'obésité et la sédentarité par pays.

    Returns:
        dataframe: dataframe contenant la révalence du manque d'activité physique par sexe et par pays 
    """
    df = pd.read_csv(DATA_PATH + "physical_activity.csv")

    df['Location'] = df['Location'].replace(mapping_countries_2)

    return df[['Location', 'Period', 'Both_sexes_val']]