import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = "data/"
RAW_DATA_PATH = "raw_data/"

def ncd_risk_pre_processing(country="Canada", rolling_window=5, sample=10):
    df = pd.read_csv(DATA_PATH + f"NCD_RisC_Nature_2026_BMI_age_standardised_{country}.csv", \
                     index_col=0)
    # print(df.index)
    df.index = df.index.astype(int)
    df_filtered = df[df.index < 2023]

    non_numeric_cols = ["Sex", "Country/Region/World", "ISO"]
    
    df_lisse = df_filtered.drop(columns=non_numeric_cols).rolling(window=rolling_window, center=True, min_periods=1).mean()

    df_final = pd.concat([df_filtered[non_numeric_cols], df_lisse], axis=1)
    df_final = df_final[df_final.index % sample == 0]

    print(df_final[["Sex", "Prevalence of BMI>=30 kg/m² (obesity)"]])

    return df_final

def load_ncd_risk():
    df = pd.read_csv(DATA_PATH + "NCD_RisC_Nature_2026_BMI_age_standardised_country-reduced.csv")

    return df

def reduce_dataset_ncd_risk(rolling_window=5, sample=10):
    df = pd.read_csv(DATA_PATH + "NCD_RisC_Nature_2026_BMI_age_standardised_country.csv")
    # print(df.index)
    # df.index = df.index.astype(int)
    # df_filtered = df[df.index < 2023]
    df_filtered = df

    target_col = "Prevalence of BMI>=30 kg/m² (obesity)"
    non_numeric_cols = ["Year", "Sex", "Country/Region/World", "ISO"]

    df_filtered = df[non_numeric_cols + [target_col]]
    df_mean = df_filtered.groupby(["Year", "Country/Region/World", "ISO"])[target_col]\
                        .mean().reset_index()
    
    df_mean["Sex"] = "Both"

    df_lisse = df_mean.drop(columns=non_numeric_cols).rolling(window=rolling_window, center=True, min_periods=1).mean()

    df_final = pd.concat([df_mean[non_numeric_cols], df_lisse], axis=1)
    df_final = df_final[df_final["Year"] % sample == 0].drop(columns="Sex")

    # print(df_final[["Sex", "Prevalence of BMI>=30 kg/m² (obesity)"]])

    df_final.to_csv(DATA_PATH + "NCD_RisC_Nature_2026_BMI_age_standardised_country-reduced.csv", index=False)

# reduce_dataset_ncd_risk()