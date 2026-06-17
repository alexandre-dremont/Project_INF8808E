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

def physical_activity_to_csv():
    df = pd.read_excel(DATA_PATH + "data.xlsx", header=2, nrows=4486)

    # Renommer pour plus de clarté
    df.columns = ["Location", "Period", "Dim2", "Both_sexes", "Male", "Female"]

    # Extraire la valeur numérique
    df["Both_sexes_val"] = df["Both_sexes"].str.extract(r"^([\d.]+)").astype(float)
    df["Female_val"] = df["Female"].str.extract(r"^([\d.]+)").astype(float)
    df["Male_val"] = df["Male"].str.extract(r"^([\d.]+)").astype(float)

    df.to_csv(DATA_PATH + "physical_activity.csv")

# physical_activity_to_csv()

def load_physical_activity():
    df = pd.read_csv(DATA_PATH + "physical_activity.csv")

    df['Location'] = df['Location'].replace(mapping_countries_2)

    return df[['Location', 'Period', 'Both_sexes_val']]

# print(load_physical_activity())