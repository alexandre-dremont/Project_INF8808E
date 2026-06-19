import pandas as pd
import plotly.express as px

DATA_PATH = "data/"

def create_heat_map(nb_countries=50):
    """Génère une Heat Map mettant en évidence une corréaltion entre différents indicateurs socio-économiques
    et la prévalence de l'obésité dans le monde
    """
    # Indicateurs
    indicator_labels = {"GDP_PPP" : "PIB par habitant en parité de pouvoir d'achat", 
                        "Health_Expenditure" : "Dépenses de santé par habitant", 
                        "Gini" : "Indice de Gini",
                        "Calories": "Apports caloriques quotidiens",
                        "Sedentary": "Sédentarité" 
    }

    df_matrix = pd.read_csv(DATA_PATH + "correlation_matrix.csv", index_col=0)

    # print(df_matrix.shape)

    # Filtrage en attendant de pouvoir sélectionner les pays
    df_matrix = df_matrix.iloc[2:, : nb_countries]

    # Renommer les lignes de la matrice
    df_matrix.index = [indicator_labels.get(ind, ind) for ind in df_matrix.index]

    fig = px.imshow(
        df_matrix, 
        labels=dict(x="Pays", y="Indicateur", color="Corrélation"), 
        color_continuous_scale="RdBu",
        range_color=[-1, 1],
        aspect="auto"
    )

    # Info-bulle
    fig.update_traces(hovertemplate=hover_template())

    fig.update_layout(
        # Style de plot
        template="plotly_white",

        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Barre de couleurs
        coloraxis_colorbar=dict(
            title=dict(
                text="Corrélation",
                font=dict(family="Inter, sans serif", size=12, color="#718096")
            ),
            tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
            outlinecolor="#e2e8f0",
            outlinewidth=1
        ),

        # Axes
        xaxis=dict(title=dict(text="Pays", 
                   font=dict(family="Inter, sans serif", size=12, color="#718096")), 
                   tickfont=dict(family="Inter, sans serif", size=12, color="#718096"),
                   gridcolor="rgba(0,0,0,0.05)"),

        yaxis=dict(title="Indicateur", tickfont=dict(family="Inter, sans serif", size=13, color="#2c3e50"),
                   ticklabelstandoff=10),
    )

    fig.update_xaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096")
    )

    fig.update_yaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
        tickangle=0,
    )

    return fig


def hover_template():
    """Génère une info-bulle complète pour étayer la Heat Map"""
    return (
        '<b>%{x}</b>'
        "<br>Indicateur : %{y}"
        "<br>Corrélation : %{z}"
        '<extra></extra>'
    )