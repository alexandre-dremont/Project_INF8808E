import plotly.graph_objects as go
from dash import Dash, dcc, html
from data_preprocessing.dumbbell_data import load_data

def make_figure():
    """
    Construit le dumbell chart orienté (flèché)
    Pour un ensemble de pays, expose le coût croissant, actuel et projeté en 2060, de l"obésité pour la société
    Ce coût est estimé en terme de perte de PIB
    """

    # Chargement des données utiles
    df = load_data()
    countries = df["Country"].tolist()
    current   = df["current_usd_ppa"].tolist()
    proj_2060 = df["cost_2060_usd_ppa"].tolist()

    # Création d"une figure vièrge
    fig = go.Figure()

    # Vecteur de variation du coût
    for i, (cur, prj) in enumerate(zip(current, proj_2060)):
        fig.add_annotation(
            x=prj-50, y=i, ax=cur+50, ay=i,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.0,
            arrowwidth=1.5, arrowcolor="#4a5568",
            text="")

    # Points actuels
    fig.add_trace(go.Scatter(
        x=current, 
        y=list(range(len(countries))),
        mode="markers",
        name="Coût actuel",
        marker=dict(color="#6b8cae", size=11),
        hovertemplate="<b>%{customdata}</b><br>Coût actuel : %{x:,.0f} $ USD PPA/hab.<extra></extra>",
        customdata=countries))

    # Points 2060
    fig.add_trace(go.Scatter(
        x=proj_2060, 
        y=list(range(len(countries))),
        mode="markers+text",
        name="Projection 2060",
        marker=dict(color="#bd4821", size=11),
        text=[f"{v:,.0f} $" for v in proj_2060],
        textposition="middle right",
        textfont=dict(family="Inter, sans serif", size=11, color="#4a5568"),
        hovertemplate="<b>%{customdata}</b><br>Projection 2060 : %{x:,.0f} $ USD PPA/hab.<extra></extra>",
        customdata=countries))

    fig.update_layout(
        # Style de page
        template="plotly_white",
        height=400,
        margin=dict(l=130, r=160, t=20, b=50),

        # Hover
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Axes 
        xaxis=dict(title=dict(text="USD PPA par habitant",
                   font=dict(family="Inter, sans serif", size=11, color="#718096")),
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   ticksuffix=" $",
                   gridcolor="rgba(0,0,0,0.05)"),
        yaxis=dict(tickvals=list(range(len(countries))), 
                   ticktext=countries,
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   ticklabelstandoff=10,
                   gridcolor="rgba(0,0,0,0.05)"),
        
        # Légende
        legend=dict(orientation="h", x=1, y=1,
                    yanchor="bottom", xanchor="right", 
                    font=dict(family="Inter, sans serif", size=12, color="#4a5568"),
                    bgcolor="rgba(0, 0, 0, 0)",
                    borderwidth=0,
                    itemsizing="constant", 
                    traceorder="normal"))
    
    return fig
