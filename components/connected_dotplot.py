import pandas as pd
import plotly.graph_objects as go
from data_preprocessing.country_labels import short_name

# Variables globales

# Equivalents des étiquettes pour passer du jeu de données au visuel final
SEX_PREFIX = {"all": "All_Adults", "male": "Males", "female": "Females"}
SEX_LABEL = {"all": "Tous adultes", "male": "Hommes", "female": "Femmes"}
MEASURE_LABEL = {"Obesity": "Obésité", "Overweight": "Surpoids"}

# Couleurs des catégories
DOT_COLORS = {"all": "#636363", "male": "#4292c6", "female": "#d6616b"}

# Utilitaires d'affichage
def value_column(sex, measure):
    return f"{SEX_PREFIX[sex]}_{measure}"



def create_connected_dotplot(dff, measure, selected):
    """
    Cette focntion est chargée de produire un connected-dots plot pour comparer le taux
    d'obésité par sexe et dans la population générale par pays.
    """
    col_all = value_column("all", measure)
    col_male = value_column("male", measure)
    col_female = value_column("female", measure)

    # Tri ascendant des pays par taux d'obésité moyen
    sub = dff.dropna(subset=[col_all]).sort_values(col_all).reset_index(drop=True)
    countries = sub["Country"].tolist()

    # Segments reliant le min au max des trois valeurs 
    x_base, y_base, x_sel, y_sel = [], [], [], []
    for _, row in sub.iterrows():
        vals = [row[c] for c in (col_all, col_male, col_female) if pd.notna(row[c])]
        if len(vals) < 2:
            continue
        seg = [min(vals), max(vals), None]
        names = [row["Country"], row["Country"], None]
        if row["Country"] == selected:
            x_sel += seg
            y_sel += names
        else:
            x_base += seg
            y_base += names


    # Création d'une nouvelle figure
    fig = go.Figure()
    # Tracé de la ligne de liaison
    fig.add_trace(go.Scatter(x=x_base, y=y_base, mode="lines",
                             line=dict(color="#d4dde8", width=1),
                             hoverinfo="skip", showlegend=False))
    if x_sel:
        fig.add_trace(go.Scatter(x=x_sel, y=y_sel, mode="lines",
                                 line=dict(color="#2c3e50", width=2.5),
                                 hoverinfo="skip", showlegend=False))


    # Ajout des points sur  le segment (homme, femme, général)
    for sex, col in (("all", col_all), ("male", col_male), ("female", col_female)):
        fig.add_trace(go.Scatter(
            # Style de scatter plot
            x=sub[col], y=sub["Country"],
            mode="markers",
            name=SEX_LABEL[sex],
            marker=dict(color=DOT_COLORS[sex],
                        size=[10 if c == selected else 7 for c in countries],
                        line=dict(width=[2 if c == selected else 0 for c in countries],
                                  color="#2c3e50")),
            customdata=sub[["Income_group", "Year"]],
            # Contenu textuel du hover
            hovertemplate=(
                "<b>%{y}</b><br>"
                f"{MEASURE_LABEL[measure]} – {SEX_LABEL[sex]} : "
                "%{x:.1f}%<br>"
                "Revenu : %{customdata[0]}<br>"
                "Enquête : %{customdata[1]}<extra></extra>")))


    # Paramétrage graphique
    fig.update_layout(

        # Style de figure
        margin=dict(l=10, r=10, t=28, b=30),
        height=max(26 * len(sub), 400),
        plot_bgcolor="white",

        # Hover
        hoverlabel=dict(bgcolor="white", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Style des axes
        xaxis=dict(title=dict(text=f"{MEASURE_LABEL[measure]} (%)",
                              font=dict(family="Inter, sans serif", size=11, color="#718096")),
                   tickfont=dict(family="Inter, sans serif", size=10, color="#718096"),
                   range=[0, 100], side="top", showgrid=True, gridcolor="#f0f4f8"),
        yaxis=dict(tickfont=dict(family="Inter, sans serif", size=8, color="#4a5568"),
                   showgrid=False, range=[-0.3, len(sub)-0.7],
                   categoryorder="array", categoryarray=countries,
                   tickmode="array", tickvals=list(range(len(countries))),
                   ticktext=[short_name(c) for c in countries]),

        # Style de légende
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="center", x=0.5,
                    font=dict(family="Inter, sans serif", size=11, color="#4a5568"),
                    bgcolor="rgba(0, 0, 0, 0)"))
    return fig
