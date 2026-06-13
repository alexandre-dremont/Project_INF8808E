import plotly.graph_objects as go

# Libellés repris dans les info-bulles
MEASURE_LABEL = {"Obesity": "Obésité", "Overweight": "Surpoids"}
# Préfixes des colonnes du CSV selon la population visée
SEX_PREFIX = {"all": "All_Adults", "male": "Males", "female": "Females"}


def create_choropleth(dff, sex, measure, selected):
    """
    Carte choroplèthe de la prévalence du surpoids et de l'obésité par pays.
    La couleur encode le pourcentage d'adultes concernés. Surbrillance sur la map du pays cliqué 
    pour le repérer d'une vue à l'autre.
    """
    col = f"{SEX_PREFIX[sex]}_{measure}"
    sub = dff.dropna(subset=[col])

    # zmax dynamique calé sur les trois populations avec une échelle figée
    # Evite que les couleurs soient écrêtées pour les pays les plus touchés

    cols = [f"{p}_{measure}" for p in SEX_PREFIX.values()]
    zmax = float(max(dff[c].max() for c in cols if c in dff.columns))

    # Surbrillance du pays sélectionné 
    # clic synchro avec le connected dot plot
    line_width = [2.2 if c == selected else 0.3 for c in sub["Country"]]
    line_color = ["#2c3e50" if c == selected else "#aaaaaa" for c in sub["Country"]]

    fig = go.Figure(go.Choropleth(
        locations=sub["Country"],
        locationmode="country names",
        z=sub[col],
        zmin=0, zmax=zmax,
        colorscale="Ice_r",
        marker_line_color=line_color,
        marker_line_width=line_width,
        customdata=sub[["Income_group", "Year"]],
        hovertemplate=(
            "<b>%{location}</b><br>"
            f"{MEASURE_LABEL[measure]} : "
            "%{z:.1f}%<br>"
            "Revenu : %{customdata[0]}<br>"
            "Enquête : %{customdata[1]}<extra></extra>"),
        colorbar=dict(title="%", thickness=12, len=0.6,
                      tickfont=dict(family="Inter, sans serif", size=10, color="#718096"))))

    fig.update_layout(
        # Projection géographique
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        # Style
        margin=dict(l=0, r=0, t=10, b=0),
        height=600,
        # Hover
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")))
    return fig
