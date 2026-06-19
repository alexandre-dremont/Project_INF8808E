import pandas as pd
import pycountry_convert as pc

DATA_PATH = "data/"

def load_ncd_risk_complete():
    """Charge les données illustrant la prévalence de l'obésité dans le monde de l'équipe NCD Risc.

    Returns:
        dataframe: prévalence de l'obésité
    """
    df = pd.read_csv(DATA_PATH + "NCD_RisC_Nature_2026_BMI_age_standardised_country.csv")

    target_col = "Prevalence of BMI>=30 kg/m² (obesity)"
    non_numeric_cols = ["Year", "Sex", "Country/Region/World", "ISO"]

    df_filtered = df[non_numeric_cols + [target_col]]
    df_mean = df_filtered.groupby(["Year", "Country/Region/World", "ISO"])[target_col]\
                        .mean().reset_index()
    
    df_mean["Sex"] = "Both"

    df_final = df_mean.drop(columns="Sex")

    return df_final

# print(load_ncd_risk_complete())

def reduce_dataset_ncd_risk(rolling_window=5, sample=10):
    """Agrège et réduit les données illustrant la prévalence de l'obésité dans le monde de l'équipe NCD Risc.
    Utilise une fenêtre glissante de 5 ans et échantionne les données tous les 10 ans.
    Génère le fichier CSV "NCD_RisC_Nature_2026_BMI_age_standardised_country-reduced.csv" stocké dans le dossier data.

    Args:
        rolling_window (int, optional): fenêtre glissante. Par défaut à 5 ans.
        sample (int, optional): nombre d'années pour l'échantillonnage. Par défaut à 10 ans.
    """
    df = pd.read_csv(DATA_PATH + "NCD_RisC_Nature_2026_BMI_age_standardised_country.csv")
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

    df_final.to_csv(DATA_PATH + "NCD_RisC_Nature_2026_BMI_age_standardised_country-reduced.csv", index=False)

# reduce_dataset_ncd_risk()

def load_ncd_risk():
    """Charge les données réduites illustrant la prévalence de l'obésité dans le monde de l'équipe NCD Risc.

    Returns:
        dataframe: prévalence de l'obésité
    """
    df = pd.read_csv(DATA_PATH + "NCD_RisC_Nature_2026_BMI_age_standardised_country-reduced.csv")
    return df


# Chargement BMI age-standardised (vues bmi_grid et timeline)

# Tranches d'IMC regroupées en 4 catégories : libellé → colonnes sources du CSV
BMI_CATEGORIES = {
    "Insuffisance pondérale": ["Prevalence of BMI<18.5 kg/m² (underweight)"],
    "Poids normal": ["Prevalence of BMI 18.5 kg/m² to <20 kg/m²",
                     "Prevalence of BMI 20 kg/m² to <25 kg/m²"],
    "Surpoids": ["Prevalence of BMI 25 kg/m² to <30 kg/m²"],
    "Obésité": ["Prevalence of BMI 30 kg/m² to <35 kg/m²",
                "Prevalence of BMI 35 kg/m² to <40 kg/m²",
                "Prevalence of BMI >=40 kg/m² (morbid obesity)"],
}

# Milieu de chaque tranche, pour estimer l'IMC moyen pondéré
BMI_MIDPOINTS = {
    "Prevalence of BMI<18.5 kg/m² (underweight)": 17.0,
    "Prevalence of BMI 18.5 kg/m² to <20 kg/m²": 19.25,
    "Prevalence of BMI 20 kg/m² to <25 kg/m²": 22.5,
    "Prevalence of BMI 25 kg/m² to <30 kg/m²": 27.5,
    "Prevalence of BMI 30 kg/m² to <35 kg/m²": 32.5,
    "Prevalence of BMI 35 kg/m² to <40 kg/m²": 37.5,
    "Prevalence of BMI >=40 kg/m² (morbid obesity)": 42.5,
}

CONTINENT_FR = {
    "Africa": "Afrique", "Asia": "Asie", "Europe": "Europe",
    "North America": "Amérique du Nord", "South America": "Amérique du Sud",
    "Oceania": "Océanie",
}
CONTINENT_OVERRIDE = {"TLS": "Asie"}   # ISO que pycountry_convert ne résout pas
_continent_cache = {}


def _iso_to_continent(iso):
    if iso not in _continent_cache:
        try:
            a2 = pc.country_alpha3_to_country_alpha2(iso)
            name = pc.convert_continent_code_to_continent_name(
                pc.country_alpha2_to_continent_code(a2))
            res = CONTINENT_FR.get(name, name)
        except Exception:
            res = "Autre"
        _continent_cache[iso] = CONTINENT_OVERRIDE.get(iso, res)   # l'override a le dernier mot
    return _continent_cache[iso]


def load_ncd_bmi(scope="country"):
    """Lit un fichier NCD-RisC brut, retire le BOM et renomme la colonne pays."""
    df = pd.read_csv(DATA_PATH + f"NCD_RisC_Nature_2026_BMI_age_standardised_{scope}.csv")
    df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]   # BOM collé à "Year"
    return df.rename(columns={"Country/Region/World": "Country"})


def load_ncd_bmi_features(scope="country"):
    """load_ncd_bmi + colonnes dérivées (Continent, IMC moyen, et les 4 catégories agrégées)."""
    df = load_ncd_bmi(scope)
    df["Continent"] = df["ISO"].map(_iso_to_continent)
    df["MeanBMI"] = sum(df[col] * mid for col, mid in BMI_MIDPOINTS.items())
    for label, cols in BMI_CATEGORIES.items():
        df[label] = df[cols].sum(axis=1)
    return df