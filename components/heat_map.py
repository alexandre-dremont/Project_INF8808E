from data_preprocessing.banque_mondiale import banque_mondiale_pre_processing
from data_preprocessing.obesity_prevalence import obesity_prevalence_pre_processing, obesity_prevalence_pre_processing_without_year
import pandas as pd
import plotly.express as px


def create_heat_map(nb_countries=10):
    df_indicator = banque_mondiale_pre_processing(scale=False).head(nb_countries)
    df_obesity = obesity_prevalence_pre_processing_without_year()

    df_obesity = df_obesity.groupby("Country")["All_Adults_Obesity"].mean().reset_index()

    df = df_indicator.merge(df_obesity, left_on="Country Name", right_on="Country")

    # Indicateurs
    indicators = ["GDP_PPP", "Health_Expenditure", "Gini"]

    df = df.dropna(subset=["Country"])

    df_matrix = df.set_index("Country")[indicators].T

    fig = px.imshow(
        df_matrix, 
        labels=dict(x="Pays", y="Indicateur", color="Valeur"), 
        color_continuous_scale="Bluyl",
        aspect="auto"
    )

    # Info-bulle
    fig.update_traces(hovertemplate=hover_template())

    return fig

def hover_template():
    '<extra></extra>'