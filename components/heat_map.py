import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DATA_PATH = "data/"

def create_heat_map():
    """Génère trois Heat maps mettant en évidence une corrélation entre différents indicateurs socio-économiques
    et la prévalence de l'obésité dans le monde
    """
    # Indicateurs
    indicator_labels = {"GDP_PPP" : "PIB par habitant en parité de pouvoir d'achat", 
                        "Health_Expenditure" : "Dépenses de santé par habitant", 
                        "Gini" : "Indice de Gini",
                        "Calories": "Apports caloriques quotidiens",
                        "Sedentary": "Sédentarité" 
    }

    # On récupère la matrice de corrélation stocké dans le fichier data
    df_matrix = pd.read_csv(DATA_PATH + "correlation_matrix.csv", index_col=0)

    selected_indicators = ["Gini", "Calories", "Sedentary"]

    # Contruction du subplot pour afficher les 3 heatmaps verticalement
    fig = make_subplots(
        rows=3, cols=1,
        vertical_spacing=0.15
    )

    for i, indicator in enumerate(selected_indicators):
        # On trie les pays par corrélation croissante pour cet indicateur 
        row_sorted = df_matrix.loc[indicator].sort_values()
        row_data = df_matrix.loc[[indicator], row_sorted.index]

        n = len(row_data.columns)
        x_positions = list(range(n))

        # Afficher la Heatmap pour l'indicateur considéré
        fig.add_trace(go.Heatmap(
            z=row_data.values,
            x=x_positions,
            y=[indicator_labels[indicator]],
            colorscale="RdBu",
            zmin=-1, zmax=1,
            showscale=(i == 0),
            hovertemplate=hover_template(),
            coloraxis="coloraxis",
            customdata=[row_data.columns.to_list()]
            ),
            row = i + 1,
            col = 1
        )

        # Afficher le nom de l'indicateur sur l'axe Y
        fig.update_yaxes(
            title=dict(
                text=indicator_labels[indicator],
                font=dict(family="Inter, sans serif", size=13, color="#2c3e50"),
            ),
            showticklabels=False,
            row = i + 1,
            col = 1
        )


    fig.update_layout(
        # Style de plot
        template="plotly_white",
        height=700,

        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Échelle de couleur
        coloraxis=dict(
            colorscale="RdBu",
            cmin=-1, cmax=1,
            colorbar=dict(
                title=dict(
                    text="Corrélation",
                    font=dict(family="Inter, sans serif", size=12, color="#2c3e50")
                ),
                tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                outlinecolor="#e2e8f0",
                outlinewidth=1
            )
        )
    )

    # Style commun à tous les axes X 
    fig.update_xaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
        tickmode="array",
        tickvals=list(range(0, n, 10)),
        ticktext=[str(v) for v in range(0, n, 10)],
        showticklabels=True,
    )

    # Seulement le dernier axe X
    fig.update_xaxes(
        title_text="Rang du pays (par corrélation croissante)",
        title_font=dict(family="Inter, sans serif", size=13, color="#2c3e50"),
        row=3, col=1
    )

    return fig


def hover_template():
    """Génère une info-bulle complète pour étayer la Heat Map"""
    return (
        '<b>%{customdata}</b>'
        "<br>Corrélation : %{z}"
        '<extra></extra>'
    )