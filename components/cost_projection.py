import plotly.graph_objects as go
from dash import Dash, dcc, html
from data_preprocessing.roi_data import load_data
import sys, os

# Gestion de l'arborescence
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def make_figure():
    """
    Cette fonction appelle les données pré-traitées pour construire un diagramme à barre horizontal.
    Ce visuel rend compte du retour sur investissement attendu d'un ensemble d'actions possibles
    pour lutter contre la prévalence de l'obésité
    """
    # Chargement des données pré-traitées
    df = load_data()

    # On attibut leur couleur à chaque barre
    colors = ["#0da781" if b else "#d34414" for b in df["rentable"]]

    # On crée le fond de la figure
    fig = go.Figure(go.Bar(
        x=df["roi"],
        y=df["action"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.1f} $" for v in df["roi"]],
        textposition="outside",
        textfont=dict(family="Inter, sans serif", color="#4a5568", size=11),
        hovertemplate="<b>%{y}</b><br>Retour : %{x:.1f} $ par $ investi<extra></extra>",
        width=0.6))

    # On signale la zone de non-rentabilité
    fig.add_vrect(
        x0=0,
        x1=1.0,
        fillcolor="rgba(186, 117, 23, 0.06)", # Apparamment nécessaire d'utiliser rgba pour manipuler la transparence
        layer="below",
        line_width=0,
    )

    # On ajoute le seuil de rentabilité
    fig.add_vline(
        x=1.0,
        line=dict(color="#d4810c", width=1),
        annotation_text="Seuil de rentabilité (1 $)",
        annotation_position="bottom right",
        annotation_font=dict(family="Inter, sans serif", color="#d4810c", size=11),
        layer="below")

    # Gestion du layout (titre, source, axes, etc.)
    fig.update_layout(

        # Style de plot
        template="plotly_white",
        bargap=0.25,
        height=380,
        margin=dict(l=230, r=80, t=20, b=50),
        showlegend=False,

        # Etiquettes
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Axes
        xaxis=dict(title=dict(text="Retour en USD PPA par dollar investi", 
                   font=dict(family="Inter, sans serif", size=12, color="#718096")), 
                   ticksuffix=" $", tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   range=[0, df["roi"].max() + 1.2], gridcolor="rgba(0,0,0,0.05)"),

        yaxis=dict(title="", tickfont=dict(family="Inter, sans serif", size=12, color="#2c3e50"),
                   ticklabelstandoff=10)
        )
    return fig
