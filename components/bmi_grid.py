from dash import dcc, html, Input, Output
import math
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pycountry_convert as pc

COUNTRY_FILE = "data/NCD_RisC_Nature_2026_BMI_age_standardised_country.csv"

# 4 catégories agrégées à partir des 7 tranches fines : (libellé, colonnes sources, couleur)
CATEGORIES = [
    ("Insuffisance pondérale",
     ["Prevalence of BMI<18.5 kg/m² (underweight)"], "#4575b4"),
    ("Poids normal",
     ["Prevalence of BMI 18.5 kg/m² to <20 kg/m²",
      "Prevalence of BMI 20 kg/m² to <25 kg/m²"], "#1a9850"),
    ("Surpoids",
     ["Prevalence of BMI 25 kg/m² to <30 kg/m²"], "#fee08b"),
    ("Obésité",
     ["Prevalence of BMI 30 kg/m² to <35 kg/m²",
      "Prevalence of BMI 35 kg/m² to <40 kg/m²",
      "Prevalence of BMI >=40 kg/m² (morbid obesity)"], "#d73027"),
]

# milieux de tranche pour estimer l'IMC moyen pondéré
BMI_MIDPOINTS = {
    "Prevalence of BMI<18.5 kg/m² (underweight)": 17.0,
    "Prevalence of BMI 18.5 kg/m² to <20 kg/m²": 19.25,
    "Prevalence of BMI 20 kg/m² to <25 kg/m²": 22.5,
    "Prevalence of BMI 25 kg/m² to <30 kg/m²": 27.5,
    "Prevalence of BMI 30 kg/m² to <35 kg/m²": 32.5,
    "Prevalence of BMI 35 kg/m² to <40 kg/m²": 37.5,
    "Prevalence of BMI >=40 kg/m² (morbid obesity)": 42.5,
}

SEX_LABEL = {"Men": "Hommes", "Women": "Femmes"}
CONTINENT_FR = {
    "Africa": "Afrique", "Asia": "Asie", "Europe": "Europe",
    "North America": "Amérique du Nord", "South America": "Amérique du Sud",
    "Oceania": "Océanie",
}
N_COLS = 8
# ISO non résolus par pycountry_convert
CONTINENT_OVERRIDE = {"TLS": "Asie"}
_continent_cache = {}


def _iso_to_continent(iso):
    if iso in _continent_cache:
        return _continent_cache[iso]
    if iso in CONTINENT_OVERRIDE:
        _continent_cache[iso] = CONTINENT_OVERRIDE[iso]
        return _continent_cache[iso]
    try:
        a2 = pc.country_alpha3_to_country_alpha2(iso)
        name = pc.convert_continent_code_to_continent_name(
            pc.country_alpha2_to_continent_code(a2))
        res = CONTINENT_FR.get(name, name)
    except Exception:
        res = "Autre"
    _continent_cache[iso] = res
    return res


def load_country_data():
    df = pd.read_csv(COUNTRY_FILE)
    df.columns = [c.strip().lstrip("﻿") for c in df.columns]
    df = df.rename(columns={"Country/Region/World": "Country"})
    df["Continent"] = df["ISO"].map(_iso_to_continent)
    df["MeanBMI"] = sum(df[col] * mid for col, mid in BMI_MIDPOINTS.items())
    for label, cols, _ in CATEGORIES:
        df[label] = df[cols].sum(axis=1)
    return df


def continents(df):
    order = ["Afrique", "Amérique du Nord", "Amérique du Sud", "Asie",
             "Europe", "Océanie", "Autre"]
    present = set(df["Continent"].unique())
    return [c for c in order if c in present]


def create_grid(df, sex, continent, sort_desc, top_n):
    d = df[df["Sex"] == sex]
    if continent != "Tous":
        d = d[d["Continent"] == continent]

    yr_min, yr_max = d["Year"].min(), d["Year"].max()
    bmi_start = d[d["Year"] == yr_min].groupby("Country")["MeanBMI"].mean()
    bmi_end   = d[d["Year"] == yr_max].groupby("Country")["MeanBMI"].mean()
    delta = (bmi_end - bmi_start).dropna()
    order = delta.sort_values(ascending=not sort_desc)
    countries = list(order.index[:top_n])
    n = len(countries)
    if n == 0:
        return go.Figure().update_layout(
            annotations=[dict(text="Aucun pays", showarrow=False)])

    CELL_H = 80    # hauteur fixe par ligne en pixels, quelle que soit N
    SPACING_PX = 28  # espace vertical fixe entre lignes (inclut les labels x)
    TOP_MARGIN = 24  # espace pour les titres de la première ligne
    n_rows = math.ceil(n / N_COLS)
    total_h = CELL_H * n_rows + SPACING_PX * max(n_rows - 1, 0) + TOP_MARGIN
    v_spacing = SPACING_PX / total_h if n_rows > 1 else 0

    titles = [f"{c} · {order[c]:+.1f}" for c in countries]
    fig = make_subplots(
        rows=n_rows, cols=N_COLS, subplot_titles=titles,
        vertical_spacing=v_spacing,
        horizontal_spacing=0.012,
    )

    for i, country in enumerate(countries):
        r, c = i // N_COLS + 1, i % N_COLS + 1
        sub = df[(df["Country"] == country) & (df["Sex"] == sex)].sort_values("Year")
        for label, _, color in CATEGORIES:
            fig.add_trace(go.Scatter(
                x=sub["Year"], y=sub[label] * 100,
                mode="lines", line=dict(width=0),
                stackgroup=f"s{i}", fillcolor=color,
                name=label, legendgroup=label, showlegend=(i == 0),
                hovertemplate=f"<b>{country}</b><br>{label} : %{{y:.1f}} %"
                              "<br>%{x}<extra></extra>",
            ), row=r, col=c)

    # ---- axes ----
    fig.update_xaxes(range=[1980, 2024], tickvals=[1990, 2000, 2010, 2020],
                     showticklabels=True, tickfont=dict(size=7), tickangle=0,
                     showgrid=False, linecolor="#ccc", linewidth=1, showline=True)
    fig.update_yaxes(range=[0, 100], tickvals=[25, 50, 75],
                     showticklabels=False, tickfont=dict(size=7),
                     showgrid=False, linecolor="#ccc", linewidth=1, showline=True)

    # grilles au-dessus des aires remplies (showgrid natif est masqué par les fills)
    shapes = []
    for i in range(n):
        xi = "" if i == 0 else str(i + 1)
        yi = "" if i == 0 else str(i + 1)
        for xval in [1990, 2000, 2010, 2020]:
            shapes.append(dict(
                type="line", layer="above",
                xref=f"x{xi}", yref=f"y{yi}",
                x0=xval, x1=xval, y0=0, y1=100,
                line=dict(color="#cccccc", width=0.6),
            ))
        for yval in [25, 50, 75]:
            shapes.append(dict(
                type="line", layer="above",
                xref=f"x{xi}", yref=f"y{yi}",
                x0=1980, x1=2024, y0=yval, y1=yval,
                line=dict(color="#cccccc", width=0.6),
            ))
    fig.update_layout(shapes=shapes)
    # labels y uniquement sur la colonne gauche
    for row in range(1, n_rows + 1):
        axis_id = "" if (row - 1) * N_COLS == 0 else str((row - 1) * N_COLS + 1)
        fig.update_layout({f"yaxis{axis_id}": dict(
            showticklabels=True,
            tickvals=[25, 50, 75], ticktext=["25%", "50%", "75%"],
        )})

    for ann in fig.layout.annotations:
        ann.font.size = 9

    LEGEND_H = 30
    # marge gauche agrandie pour les labels y de la colonne gauche
    fig.update_layout(
        height=total_h + LEGEND_H,
        margin=dict(l=28, r=4, t=TOP_MARGIN, b=LEGEND_H),
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="top", y=0, x=0,
                    font=dict(size=12), tracegroupgap=0),
        hovermode="closest",
    )
    return fig


def build_layout(df):
    return html.Div([
        html.Div([
            html.Div([
                html.Label("Population", style={"fontWeight": "bold", "marginRight": "8px", "fontSize": "15px"}),
                dcc.RadioItems(
                    id="grid-sex",
                    options=[{"label": SEX_LABEL[k], "value": k} for k in ["Men", "Women"]],
                    value="Men", inline=True, labelStyle={"marginRight": "12px", "fontSize": "15px"}),
            ], style={"display": "inline-block", "marginRight": "28px", "verticalAlign": "top"}),

            html.Div([
                html.Label("Continent", style={"fontWeight": "bold", "marginRight": "8px", "fontSize": "15px"}),
                dcc.Dropdown(id="grid-continent", value="Tous", clearable=False,
                             options=[{"label": "Tous", "value": "Tous"}]
                             + [{"label": c, "value": c} for c in continents(df)],
                             style={"width": "190px"}),
            ], style={"display": "inline-block", "marginRight": "28px", "verticalAlign": "top"}),

            html.Div([
                html.Label("Trier", style={"fontWeight": "bold", "marginRight": "8px", "fontSize": "15px"}),
                dcc.RadioItems(
                    id="grid-sort",
                    options=[{"label": "Variation la plus forte d'abord", "value": "desc"},
                             {"label": "Variation la plus faible d'abord", "value": "asc"}],
                    value="desc", inline=True, labelStyle={"marginRight": "12px", "fontSize": "15px"}),
            ], style={"display": "inline-block", "marginRight": "28px", "verticalAlign": "top"}),

            html.Div([
                html.Label("Nombre de pays", style={"fontWeight": "bold", "fontSize": "15px"}),
                dcc.Slider(id="grid-topn", min=25, max=100, step=None, value=50,
                           marks={25: "25", 50: "50", 100: "100"}),
            ], style={"display": "inline-block", "width": "320px", "verticalAlign": "top"}),
        ], style={"marginBottom": "12px"}),

        html.Div(
            dcc.Graph(id="grid-figure", config={"responsive": False}),
            style={"maxHeight": "640px", "overflowY": "scroll",
                   "border": "1px solid #eee"},
        ),
    ], style={"maxWidth": "1300px", "margin": "0 auto", "fontFamily": "sans-serif"})


def register_callbacks(app, df):
    @app.callback(
        Output("grid-figure", "figure"),
        Input("grid-sex", "value"),
        Input("grid-continent", "value"),
        Input("grid-sort", "value"),
        Input("grid-topn", "value"),
    )
    def update_grid(sex, continent, sort, top_n):
        return create_grid(df, sex, continent, sort == "desc", top_n)
