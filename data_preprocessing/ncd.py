import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = "data/"

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
