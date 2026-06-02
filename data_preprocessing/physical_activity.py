import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = "data/"

def physical_activity_pre_processing(annee=2019):
    df = pd.read_excel(DATA_PATH + "physical_activity.csv")

    df_annee = df[df["Period"]==annee]

    cols_to_normalize = ["Both_sexes_val", "Male_val", "Female_val"]

    scaler = MinMaxScaler()
    df_norm = df_annee.copy()
    df_norm[cols_to_normalize] = scaler.fit_transform(df_annee[cols_to_normalize])

    df_norm.replace("United States of America", "United States", inplace=True)

    return df_norm

# print(physical_activity_pre_processing().tail(15))


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