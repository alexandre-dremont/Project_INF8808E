import pandas as pd
from data_preprocessing.dietary_compositions import load_data_dietary_compositions
from data_preprocessing.ncd import load_ncd_risk

# Constantes
ALL_FOOD_CATEGORIES = ["Boissons alcoolisées", "Sucre", "Huiles et graisses", "Viande",
    "Produits laitiers et œufs", "Fruits et légumes", "Racines féculentes",
    "Légumineuses", "Céréales et grains", "Autres", "Total"]

OBESITY_COL = "Prevalence of BMI>=30 kg/m² (obesity)"

# Correspondance pays continent
COUNTRY_CONTINENT = {
    "Afghanistan": "Asie", "Albania": "Europe", "Algeria": "Afrique",
    "Angola": "Afrique", "Argentina": "Amérique du Sud", "Armenia": "Asie",
    "Australia": "Océanie", "Austria": "Europe", "Azerbaijan": "Asie",
    "Bahrain": "Asie", "Bangladesh": "Asie", "Belarus": "Europe",
    "Belgium": "Europe", "Benin": "Afrique", "Bolivia": "Amérique du Sud",
    "Bosnia and Herzegovina": "Europe", "Botswana": "Afrique", "Brazil": "Amérique du Sud",
    "Bulgaria": "Europe", "Burkina Faso": "Afrique", "Burundi": "Afrique",
    "Cambodia": "Asie", "Cameroon": "Afrique", "Canada": "Amérique du Nord",
    "Central African Republic": "Afrique", "Chad": "Afrique", "Chile": "Amérique du Sud",
    "China": "Asie", "Colombia": "Amérique du Sud", "Congo": "Afrique",
    "Costa Rica": "Amérique du Nord", "Croatia": "Europe", "Cuba": "Amérique du Nord",
    "Cyprus": "Europe", "Czech Republic": "Europe", "Denmark": "Europe",
    "Dominican Republic": "Amérique du Nord", "Ecuador": "Amérique du Sud",
    "Egypt": "Afrique", "El Salvador": "Amérique du Nord", "Estonia": "Europe",
    "Ethiopia": "Afrique", "Finland": "Europe", "France": "Europe",
    "Gabon": "Afrique", "Georgia": "Asie", "Germany": "Europe",
    "Ghana": "Afrique", "Greece": "Europe", "Guatemala": "Amérique du Nord",
    "Guinea": "Afrique", "Haiti": "Amérique du Nord", "Honduras": "Amérique du Nord",
    "Hungary": "Europe", "India": "Asie", "Indonesia": "Asie",
    "Iran": "Asie", "Iraq": "Asie", "Ireland": "Europe",
    "Israel": "Asie", "Italy": "Europe", "Jamaica": "Amérique du Nord",
    "Japan": "Asie", "Jordan": "Asie", "Kazakhstan": "Asie",
    "Kenya": "Afrique", "Kuwait": "Asie", "Kyrgyzstan": "Asie",
    "Laos": "Asie", "Latvia": "Europe", "Lebanon": "Asie",
    "Libya": "Afrique", "Lithuania": "Europe", "Luxembourg": "Europe",
    "Madagascar": "Afrique", "Malawi": "Afrique", "Malaysia": "Asie",
    "Mali": "Afrique", "Malta": "Europe", "Mauritania": "Afrique",
    "Mauritius": "Afrique", "Mexico": "Amérique du Nord", "Moldova": "Europe",
    "Mongolia": "Asie", "Morocco": "Afrique", "Mozambique": "Afrique",
    "Myanmar": "Asie", "Namibia": "Afrique", "Nepal": "Asie",
    "Netherlands": "Europe", "New Zealand": "Océanie", "Nicaragua": "Amérique du Nord",
    "Niger": "Afrique", "Nigeria": "Afrique", "North Macedonia": "Europe",
    "Norway": "Europe", "Oman": "Asie", "Pakistan": "Asie",
    "Panama": "Amérique du Nord", "Paraguay": "Amérique du Sud", "Peru": "Amérique du Sud",
    "Philippines": "Asie", "Poland": "Europe", "Portugal": "Europe",
    "Qatar": "Asie", "Romania": "Europe", "Russia": "Europe",
    "Rwanda": "Afrique", "Saudi Arabia": "Asie", "Senegal": "Afrique",
    "Serbia": "Europe", "Sierra Leone": "Afrique", "Singapore": "Asie",
    "Slovakia": "Europe", "Slovenia": "Europe", "Somalia": "Afrique",
    "South Africa": "Afrique", "South Korea": "Asie", "Spain": "Europe",
    "Sri Lanka": "Asie", "Sudan": "Afrique", "Sweden": "Europe",
    "Switzerland": "Europe", "Syria": "Asie", "Taiwan": "Asie",
    "Tajikistan": "Asie", "Tanzania": "Afrique", "Thailand": "Asie",
    "Togo": "Afrique", "Trinidad and Tobago": "Amérique du Nord", "Tunisia": "Afrique",
    "Turkey": "Europe", "Turkmenistan": "Asie", "Uganda": "Afrique",
    "Ukraine": "Europe", "United Arab Emirates": "Asie", "United Kingdom": "Europe",
    "United States": "Amérique du Nord", "Uruguay": "Amérique du Sud",
    "Uzbekistan": "Asie", "Venezuela": "Amérique du Sud", "Vietnam": "Asie",
    "Yemen": "Asie", "Zambia": "Afrique", "Zimbabwe": "Afrique",
}
 
CONTINENT_ORDER = ["Tous", "Afrique", "Amérique du Nord", "Amérique du Sud",
                   "Asie", "Europe", "Océanie"]


# Chargement des données
def load_slope_data():
    """Charge et fusionne dietary + obesity et
    Retourne (df, available_countries)"""

    df_dietary = load_data_dietary_compositions()
    df_obesity = load_ncd_risk()

    df = df_dietary.merge(df_obesity, left_on=["Code", "Year"], right_on=["ISO", "Year"], how="left")\
                    .drop(columns=["ISO", "Country/Region/World"])
    
    obesity_start = df[df["Year"] == 1980].set_index("Entity")[OBESITY_COL]
    obesity_end   = df.groupby("Entity")["Year"].max().reset_index()
    obesity_end   = df.merge(obesity_end, on=["Entity", "Year"]).set_index("Entity")[OBESITY_COL]
    df["obesity_delta"] = df["Entity"].map(obesity_end - obesity_start)
 
    # Continent
    df["Continent"] = df["Entity"].map(COUNTRY_CONTINENT).fillna("Autre")
    
    # Pays disponibles
    countries_with_obesity = df[
        (df["Year"] == 1980) & (df[OBESITY_COL].notna())
        ]["Entity"].unique()
 
    all_countries = df["Entity"].unique()
    available_countries = [c for c in all_countries if c in countries_with_obesity]
 
    return df, available_countries


# Layout

def filtered_sorted(available_countries, df, continent, sort):
    """Retourne la liste des pays filtrée par continent et triée"""
    filtered = [c for c in available_countries
        if continent == "Tous" or COUNTRY_CONTINENT.get(c) == continent]
    
    if sort != "none" and filtered:
        deltas = (
            df[df["Entity"].isin(filtered)]
            .drop_duplicates("Entity")
            .set_index("Entity")["obesity_delta"])
        
        filtered = sorted(
            filtered,
            key=lambda c: deltas.get(c, 0),
            reverse=(sort == "desc"))
        
    return filtered