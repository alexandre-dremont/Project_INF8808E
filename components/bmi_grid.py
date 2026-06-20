from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_preprocessing.ncd import load_ncd_bmi_features, BMI_CATEGORIES


# Variables globales pour la figure

# Palette de couluer par IMC
CATEGORY_COLORS = {
    "Insuffisance pondérale": "#9ca1e6",
    "Poids normal": "#78b986",
    "Surpoids": "#f0ad7a",
    "Obésité": "#CC444F",
}

# Catégories par variable
SEX_LABEL = {"Men": "Hommes", "Women": "Femmes"}
CONTINENT_ORDER = ["Afrique", "Amérique du Nord", "Amérique du Sud", "Asie", "Europe", "Océanie", "Autre"]

# Paramètres à ajuster
N_COLS = 8
YEAR_RANGE = [1980, 2024]
# Graduations verticales communes aux vignettes
GRID_X = [1990, 2000, 2010, 2020] 
# graduations horizontales (en %)
GRID_Y = [25, 50, 75] 

# Utilitaires divers (données et visuels)
def load_country_data():
    """ Chargement des données"""
    return load_ncd_bmi_features("country")

def continents(df):
    """Construction de la liste des pays par continent"""
    present = set(df["Continent"].unique())
    return [c for c in CONTINENT_ORDER if c in present]

def _axis_suffix(n):
    """Extrait le suffixe pays pour identification dans figure"""
    return "" if n == 1 else str(n)


# Création d'une mosaïque de figures (small multiples)
def create_grid(df, sex, continent, sort_desc, top_n):
    """
    Fonction chargée de créer un small multiples par pays de la distribution
    au cours du temps de l'IMC par pays suivant les 4 catégories de poids définies plus haut.
    Les distributions au cours du temps seront présentées sous la forme d'un stacked area chart
    (diagramme à surfaces empilées).
    """

    # On réduit les données utiles
    d = df[df["Sex"] == sex]
    if continent != "Tous":
        d = d[d["Continent"] == continent]

    # Variation de l'IMC moyen entre 1980 et 2024 donne l'ordre du classement
    yr_min, yr_max = d["Year"].min(), d["Year"].max()
    bmi_start = d[d["Year"] == yr_min].groupby("Country")["MeanBMI"].mean()
    bmi_end = d[d["Year"] == yr_max].groupby("Country")["MeanBMI"].mean()
    delta = (bmi_end - bmi_start).dropna().sort_values(ascending=not sort_desc)
    countries = list(delta.index[:top_n])
    n = len(countries)

    # Paramètre des vignettes
    n_rows = -(-n // N_COLS)
    total_h = 80 * n_rows + 28 * max(n_rows - 1, 0) + 24
    v_spacing = 28 / total_h if n_rows > 1 else 0

    titles = [f"{c} · {delta[c]:+.1f}" for c in countries]
    fig = make_subplots(rows=n_rows, cols=N_COLS, subplot_titles=titles,
                        vertical_spacing=v_spacing, horizontal_spacing=0.012)

    for i, country in enumerate(countries):
        r, c = i // N_COLS + 1, i % N_COLS + 1
        sub = df[(df["Country"] == country) & (df["Sex"] == sex)].sort_values("Year")
        for label in BMI_CATEGORIES:
            fig.add_trace(go.Scatter(
                x=sub["Year"], y=sub[label] * 100,
                mode="lines", line=dict(width=0),
                stackgroup=f"s{i}", fillcolor=CATEGORY_COLORS[label],
                name=label, legendgroup=label, showlegend=(i == 0),
                hovertemplate=f"<b>{country}</b><br>{label} : %{{y:.1f}} %"
                              "<br>%{x}<extra></extra>",
            ), row=r, col=c)

    fig.update_xaxes(range=YEAR_RANGE, tickvals=GRID_X, showticklabels=True,
                     tickfont=dict(size=7), tickangle=0, showgrid=False,
                     showline=True, linecolor="#ccc", linewidth=1)
    fig.update_yaxes(range=[0, 100], tickvals=GRID_Y, showticklabels=False,
                     tickfont=dict(size=7), showgrid=False,
                     showline=True, linecolor="#ccc", linewidth=1)

    # Les aires empilées masquent la grille native
    # On la redessine par-dessus
    grid_line = dict(color="#cccccc", width=0.6)
    shapes = []
    for i in range(n):
        s = _axis_suffix(i + 1)
        shapes += [dict(type="line", layer="above", xref=f"x{s}", yref=f"y{s}",
                        x0=x, x1=x, y0=0, y1=100, line=grid_line) for x in GRID_X]
        shapes += [dict(type="line", layer="above", xref=f"x{s}", yref=f"y{s}",
                        x0=YEAR_RANGE[0], x1=YEAR_RANGE[1], y0=y, y1=y, line=grid_line)
                   for y in GRID_Y]
    fig.update_layout(shapes=shapes)

    # Étiquettes Y seulement sur la colonne de gauche pour ne pas surcharger
    for row in range(1, n_rows + 1):
        s = _axis_suffix((row - 1) * N_COLS + 1)
        fig.update_layout({f"yaxis{s}": dict(showticklabels=True, tickvals=GRID_Y,
                                             ticktext=[f"{y}%" for y in GRID_Y])})

    fig.update_annotations(font=dict(size=9))

    fig.update_layout(
        height=total_h + 30,
        margin=dict(l=28, r=4, t=24, b=30),
        plot_bgcolor="white",
        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),
        legend=dict(orientation="h", yanchor="top", y=0, x=0,
                    font=dict(size=12), tracegroupgap=0))
    return fig



# Rendu final du visuel
def build_layout(df):
    label_style = {"fontSize": "11px", "fontWeight": "600", "letterSpacing": "1px",
                   "textTransform": "uppercase", "color": "#6b8cae",
                   "marginRight": "8px", "fontFamily": "Inter, sans serif"}
    radio_style = {"marginRight": "12px", "fontSize": "13px",
                   "color": "#4a5568", "fontFamily": "Inter, sans serif"}
    block_style = {"display": "inline-block", "marginRight": "28px", "verticalAlign": "top"}

    return html.Div([
        html.Div([
            html.Div([
                html.Label("Population", style=label_style),
                dcc.RadioItems(id="grid-sex", value="Men", inline=True, labelStyle=radio_style,
                               options=[{"label": SEX_LABEL[k], "value": k} for k in ("Men", "Women")]),
            ], style=block_style),

            html.Div([
                html.Label("Continent", style=label_style),
                dcc.Dropdown(id="grid-continent", value="Tous", clearable=False,
                             options=[{"label": "Tous", "value": "Tous"}]
                                     + [{"label": c, "value": c} for c in continents(df)],
                             style={"width": "190px", "fontSize": "13px", "fontFamily": "Inter, sans serif"}),
            ], style=block_style),

            html.Div([
                html.Label("Trier", style=label_style),
                dcc.RadioItems(id="grid-sort", value="desc", inline=True, labelStyle=radio_style,
                               options=[{"label": "Variation la plus forte d'abord", "value": "desc"},
                                        {"label": "Variation la plus faible d'abord", "value": "asc"}]),
            ], style=block_style),

            html.Div([
                html.Label("Nombre de pays", style=label_style),
                dcc.Slider(id="grid-topn", min=25, max=100, step=None, value=50,
                           marks={25: "25", 50: "50", 100: "100"}),
            ], style={"display": "inline-block", "width": "320px", "verticalAlign": "top"}),
        ], style={"marginBottom": "12px"}),

        html.Div(dcc.Graph(id="grid-figure", config={"responsive": False}),
                 style={"maxHeight": "640px", "overflowY": "scroll", "border": "1px solid #eee"}),
    ], style={"maxWidth": "1300px", "margin": "0 auto", "fontFamily": "Inter, sans serif"})



# Callbacks
def register_callbacks(app, df):
    @app.callback(
        Output("grid-figure", "figure"),
        Input("grid-sex", "value"),
        Input("grid-continent", "value"),
        Input("grid-sort", "value"),
        Input("grid-topn", "value"))
    def update_grid(sex, continent, sort, top_n):
        return create_grid(df, sex, continent, sort == "desc", top_n)
