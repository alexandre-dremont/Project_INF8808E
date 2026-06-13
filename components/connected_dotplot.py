import pandas as pd
import plotly.graph_objects as go

SEX_PREFIX = {"all": "All_Adults", "male": "Males", "female": "Females"}
SEX_LABEL = {"all": "Tous adultes", "male": "Hommes", "female": "Femmes"}
MEASURE_LABEL = {"Obesity": "Obésité", "Overweight": "Surpoids"}
# Une couleur par population : gris neutre pour « tous », bleu/rouge pour H/F
DOT_COLORS = {"all": "#636363", "male": "#4292c6", "female": "#d6616b"}

def value_column(sex, measure):
    return f"{SEX_PREFIX[sex]}_{measure}"

def create_connected_dotplot(dff, measure, selected):
    """
    Connected dot plot : un pays par ligne, trié par prévalence « tous adultes ».
    Chaque ligne relie les valeurs hommes / femmes / tous, ce qui donne à lire
    d'un coup d'œil l'écart entre sexes. Vue couplée à la carte (clic partagé).
    """
    col_all = value_column("all", measure)
    col_male = value_column("male", measure)
    col_female = value_column("female", measure)

    # Tri ascendant : les pays les plus touchés se retrouvent en haut du classement
    sub = dff.dropna(subset=[col_all]).sort_values(col_all).reset_index(drop=True)
    countries = sub["Country"].tolist()

    # Segments reliant le min au max des trois valeurs (None = rupture de ligne).
    # On met de côté le pays sélectionné pour le retracer par-dessus, en plus épais.
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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_base, y=y_base, mode="lines",
                             line=dict(color="#d4dde8", width=1),
                             hoverinfo="skip", showlegend=False))
    if x_sel:
        fig.add_trace(go.Scatter(x=x_sel, y=y_sel, mode="lines",
                                 line=dict(color="#2c3e50", width=2.5),
                                 hoverinfo="skip", showlegend=False))

    # Un nuage de points par population, posé sur les segments
    for sex, col in (("all", col_all), ("male", col_male), ("female", col_female)):
        fig.add_trace(go.Scatter(
            x=sub[col], y=sub["Country"],
            mode="markers",
            name=SEX_LABEL[sex],
            marker=dict(color=DOT_COLORS[sex],
                        size=[10 if c == selected else 7 for c in countries],
                        line=dict(width=[2 if c == selected else 0 for c in countries],
                                  color="#2c3e50")),
            customdata=sub[["Income_group", "Year"]],
            hovertemplate=(
                "<b>%{y}</b><br>"
                f"{MEASURE_LABEL[measure]} – {SEX_LABEL[sex]} : "
                "%{x:.1f}%<br>"
                "Revenu : %{customdata[0]}<br>"
                "Enquête : %{customdata[1]}<extra></extra>")))

    fig.update_layout(
        # Style
        margin=dict(l=10, r=10, t=28, b=30),
        height=max(26 * len(sub), 400),
        plot_bgcolor="white",
        # Hover
        hoverlabel=dict(bgcolor="white", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),
        # Axes avec graduations en haut pour suivre le regard depuis le titre
        xaxis=dict(title=dict(text=f"{MEASURE_LABEL[measure]} (%)",
                              font=dict(family="Inter, sans serif", size=11, color="#718096")),
                   tickfont=dict(family="Inter, sans serif", size=10, color="#718096"),
                   range=[0, 100], side="top", showgrid=True, gridcolor="#f0f4f8"),
        yaxis=dict(tickfont=dict(family="Inter, sans serif", size=10, color="#4a5568"),
                   showgrid=False, range=[-0.3, len(sub) - 0.7],
                   categoryorder="array", categoryarray=countries),
        # Légende
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="center", x=0.5,
                    font=dict(family="Inter, sans serif", size=11, color="#4a5568"),
                    bgcolor="rgba(0, 0, 0, 0)"))
    return fig
