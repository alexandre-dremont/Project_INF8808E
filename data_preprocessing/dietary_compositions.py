import pandas as pd

DATA_PATH = "data/"
RAW_DATA_PATH = "raw_data/"

def dietary_compositions_pre_processing_total(annee=2019):
    df = pd.read_csv(DATA_PATH + "dietary-compositions-by-commodity-group.csv")
    df_annee = df[df["Year"]==annee][["Entity", "Code"]]
    df_annee["Total"] = df.iloc[:,2:].sum(axis=1)

    df_annee["Total"] = (df_annee["Total"]-df_annee["Total"].min())/(df_annee["Total"].max()-df_annee["Total"].min())

    return df_annee

# print(dietary_compositions_pre_processing_total())

def dietary_compositions_pre_processing(rolling_window=5, sample=10):
    df = pd.read_csv(DATA_PATH + "dietary-compositions-by-commodity-group.csv", index_col=2)

    non_numeric_cols = ["Entity", "Code"]

    df_lisse = df.drop(columns=non_numeric_cols).rolling(window=rolling_window, center=True, min_periods=1).mean()

    df_final = pd.concat([df[non_numeric_cols], df_lisse], axis=1)
    df_final = df_final[df_final.index % sample == 0]

    # print(df_final)

    return df_final

# print(dietary_compositions_pre_processing().columns)

def reduce_dietary_compositions_dataset(rolling_window=5, sample=10):
    df = pd.read_csv(RAW_DATA_PATH + "dietary-compositions-by-commodity-group.csv")

    non_numeric_cols = ["Entity", "Code", "Year"]
    countries = df["Entity"].unique()

    # df[["Alcoholic beverages", "Pulses"]] = df[["Alcoholic beverages", "Pulses"]].fillna(0)

    # print(df.isna().sum())

    df["Total"] = df.iloc[:,2:].sum(axis=1)

    results = []

    for country in countries:
        df_country = df[df["Entity"]==country].sort_values("Year")

        df_lisse = df_country.drop(columns=non_numeric_cols).rolling(window=rolling_window, 
                        center=True, min_periods=1).mean()
        
        first_value = df_lisse.iloc[0]
        df_variation = (df_lisse - first_value) / first_value

        df_variation = df_variation.replace(float("inf"), pd.NA)

        df_final = pd.concat([
            df_country[non_numeric_cols].reset_index(drop=True), 
            df_variation.reset_index(drop=True)
        ], axis=1)
        df_final = df_final[df_final["Year"] % sample == 0]

        results.append(df_final)

    df_all = pd.concat(results, ignore_index=True)

    df_all.to_csv(DATA_PATH + "dietary-compositions-by-commodity-group-reduced.csv", index=False)

# def reduce_dietary_compositions_dataset(rolling_window=5, sample=10):
#     df = pd.read_csv(RAW_DATA_PATH + "dietary-compositions-by-commodity-group.csv")

#     non_numeric_cols = ["Entity", "Code", "Year"]
#     countries = df["Entity"].unique()

#     df["Total"] = df.iloc[:,2:].sum(axis=1)

#     results = []

#     for country in countries:
#         df_country = df[df["Entity"]==country].sort_values("Year")

#         df_lisse = df_country.drop(columns=non_numeric_cols).rolling(window=rolling_window, 
#                         center=True, min_periods=1).mean()

#         df_final = pd.concat([
#             df_country[non_numeric_cols].reset_index(drop=True), 
#             df_lisse.reset_index(drop=True)
#         ], axis=1)
#         df_final = df_final[df_final["Year"] % sample == 0]

#         results.append(df_final)

#     df_all = pd.concat(results, ignore_index=True)

#     df_all.to_csv(DATA_PATH + "dietary-compositions-by-commodity-group-reduced.csv", index=False)

# reduce_dietary_compositions_dataset()


def load_data_dietary_compositions():

    df = pd.read_csv(DATA_PATH + "dietary-compositions-by-commodity-group-reduced.csv")

    return df

# print(load_data_dietary_compositions())
