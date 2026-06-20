from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
from data_preprocessing.ncd import load_ncd_bmi


# Variables globales 

# Traduction des genre
SEX_LABEL = {"Men": "Hommes", "Women": "Femmes", "All": "Tous adultes"}

# Etiquettes de catégories et type de ligne associé
OBESITY = ("Prevalence of BMI>=30 kg/m² (obesity)", "Obésité (IMC ≥ 30 kg/m²)", "solid")
MORBID = ("Prevalence of BMI >=40 kg/m² (morbid obesity)", "Obésité morbide (IMC ≥ 40 kg/m²)", "dot")

# Variables de style (couleurs, type de lignes)
ALL_COLOR = "#2c3e50"
ALL_BAND = "rgba(44,62,80,0.08)"
SEX_COLORS = {
    "Men":   {"active": "#a47299", "band": "rgba(74,114,153,0.12)",
              "inactive": "rgba(74,114,153,0.25)"},
    "Women": {"active": "#bd4821", "band": "rgba(189,72,33,0.12)",
              "inactive": "rgba(189,72,33,0.25)"},
}
COUNTRY_STYLES = ["solid", "dash"]
NO_COUNTRY = "__none__"


# Traitement des données pour visualisation
def _display_name(country):
    """Traduction de World à Monde"""
    return "Monde" if country == "World" else country

def load_ncd_data():
    """Concatènation des estimations Monde par pays en une table unique"""
    return pd.concat([load_ncd_bmi("world"), load_ncd_bmi("country")], ignore_index=True)

def _filter(df, country, sex):
    """Filtrage et tri du jeu de données par pays et sexe selon la selection"""
    return df[(df["Country"] == country) & (df["Sex"] == sex)].sort_values("Year")

def _all_adults(df, country):
    """Création de la variable All à partir des données par genre"""
    sub = df[df["Country"] == country]
    num_cols = [c for c in sub.select_dtypes("number").columns if c != "Year"]
    avg = sub.groupby("Year")[num_cols].mean().reset_index()
    avg["Country"] = country
    return avg



# Utilitaires pour créer la figure
def _font(size, color="#718096"):
    """Style de texte"""
    return dict(family="Inter, sans serif", size=size, color=color)

def _add_ci(fig, dff, base, band_color):
    """Fonction chargée de produire les intervalle de confiance"""
    lo, hi = base + " lower 95% uncertainty interval", base + " upper 95% uncertainty interval"
    if lo not in dff.columns or hi not in dff.columns:
        return
    fig.add_trace(go.Scatter(x=dff["Year"], y=dff[hi] * 100, mode="lines",
                             line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=dff["Year"], y=dff[lo] * 100, mode="lines",
                             line=dict(width=0), fill="tonexty", fillcolor=band_color,
                             showlegend=False, hoverinfo="skip"))

def _add_line(fig, dff, base, name, color, dash, width=2.0):
    """Construit les courbes pour les variables selectionnées"""
    fig.add_trace(go.Scatter(
        x=dff["Year"], y=dff[base] * 100, mode="lines",
        line=dict(width=width, color=color, dash=dash), name=name,
        hovertemplate=f"{name}<br>%{{x}} : %{{y:.1f}} %<extra></extra>"))

def _draw_country(fig, df, country, selected_sex, series, line_style=None, label_prefix=""):
    """Gestion de l'affichage des variables selon le sexe coché et les pays choisis"""
    prefix = f"{label_prefix} - " if label_prefix else ""

    # Si les données concernent la poulation générale 
    if selected_sex == "All":
        dff = _all_adults(df, country)
        for base, label, dash in series:
            _add_ci(fig, dff, base, ALL_BAND)
            _add_line(fig, dff, base, f"{prefix}{label} - Tous adultes",
                      ALL_COLOR, line_style or dash, width=2.3)
        return dff

    # Si les données à présenter concernent un sexe en particulier
    # On laisse les données relatives à l'autre sexe en transparence derrière
    other = "Women" if selected_sex == "Men" else "Men"
    dff_active, dff_other = _filter(df, country, selected_sex), _filter(df, country, other)
    for base, label, dash in series:
        d = line_style or dash
        _add_line(fig, dff_other, base, f"{prefix}{label} - {SEX_LABEL[other]}",
                  SEX_COLORS[other]["inactive"], d, width=1.3)
        _add_ci(fig, dff_active, base, SEX_COLORS[selected_sex]["band"])
        _add_line(fig, dff_active, base, f"{prefix}{label} - {SEX_LABEL[selected_sex]}",
                  SEX_COLORS[selected_sex]["active"], d, width=2.0)
    return dff_active




# Construction de la figure
def create_obesity_trend(df, country1, country2, selected_sex, metric):
    """
    Fonction chargée de construire le visuel à partir des données, de la selection de l'utilisateur
    et des utlitaires définis plus haut.
    """
    series = [MORBID] if metric == "morbid" else [OBESITY]
    comparing = country2 and country2 != NO_COUNTRY
    fig = go.Figure()

    if comparing:
        ann_color = ALL_COLOR if selected_sex == "All" else SEX_COLORS[selected_sex]["active"]
        for country, line_style in zip([country1, country2], COUNTRY_STYLES):
            dff = _draw_country(fig, df, country, selected_sex, series,
                                line_style, label_prefix=_display_name(country))
            # Nom du pays posé en bout de courbe à la dernière année connue
            last = dff[dff["Year"] == dff["Year"].max()]
            if not last.empty:
                fig.add_annotation(
                    x=2024, y=last[series[0][0]].iloc[0] * 100,
                    text=f"<b>{_display_name(country)}</b>",
                    xanchor="left", yanchor="middle", showarrow=False, xshift=6,
                    font=_font(10, ann_color))
    else:
        _draw_country(fig, df, country1, selected_sex, series)


    fig.update_layout(
        # Style de la page du visuel
        template="plotly_white",
        plot_bgcolor="white",
        margin=dict(l=60, r=80, t=50, b=40),
        height=420,

        # Hover au survol
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0", font=_font(11, "#2c3e50")),
        
        # Axes
        xaxis=dict(title=dict(text="Année", font=_font(11)), tickfont=_font(11),
                   range=[1980, 2030], tickvals=[1980, 1990, 2000, 2010, 2020, 2024],
                   gridcolor="#f0f4f8"),
        yaxis=dict(title=dict(text="Part de la population", font=_font(11)), tickfont=_font(11),
                   rangemode="tozero", ticksuffix=" %", gridcolor="#f0f4f8"),
        
        # Légende
        legend=dict(font=_font(10, "#4a5568"), orientation="h",
                    yanchor="top", y=-0.15, xanchor="center", x=0.5))
    return fig




# Création du rendu global de la figure 
def build_layout(df):
    """Fonction chargée du rendu
    Ajoute les boutons et leur style
    Contrôle le style du visuel dans la page"""
    countries = sorted(df["Country"].unique())
    if "World" in countries:      
        countries = ["World"] + [c for c in countries if c != "World"]
    options = [{"label": _display_name(c), "value": c} for c in countries]
    compare_options = [{"label": "- aucun -", "value": NO_COUNTRY}] + options

    # Style des étiquettes
    label_style = {"fontSize": "11px", "fontWeight": "600", "letterSpacing": "1px",
                   "textTransform": "uppercase", "color": "#6b8cae",
                   "marginRight": "8px", "fontFamily": "Inter, sans serif"}
    # Style des boutons radio
    radio_style = {"marginRight": "12px", "fontSize": "13px",
                   "color": "#4a5568", "fontFamily": "Inter, sans serif"}
    # Style du menu de selection
    menu_style = {"width": "190px", "fontSize": "13px", "fontFamily": "Inter, sans serif"}
    # Style des blocs
    block_style = {"display": "inline-block", "marginRight": "32px",
                   "alignItems": "center", "verticalAlign": "top"}

    # Gestion de la configuration des boutons Plotly disponibles d'office
    graph_config = {
        "modeBarButtonsToRemove": ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
                                   "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian",
                                   "toggleSpikelines", "lasso2d", "select2d"],
        "toImageButtonOptions": {"format": "png", "filename": "evolution_obesite",
                                 "width": 1200, "height": 500, "scale": 2}}


    # Ajout des menus et boutons de configuration du visuel
    return html.Div([
        html.Div([
            html.Div([
                # Pays 1
                html.Label("Pays", style=label_style),
                dcc.Dropdown(id="q2-country", options=options, value="United States of America",
                             clearable=False, searchable=True, style=menu_style),
            ], style=block_style),

            html.Div([
                # Pays 2
                html.Label("Comparer avec", style=label_style),
                dcc.Dropdown(id="q2-country2", options=compare_options, value="China",
                             clearable=False, searchable=True, style=menu_style),
            ], style=block_style),

            html.Div([
                # Genre
                html.Label("Sexe", style=label_style),
                dcc.RadioItems(id="q2-sex", value="All", inline=True, labelStyle=radio_style,
                               options=[{"label": SEX_LABEL[k], "value": k}
                                        for k in ("Men", "Women", "All")]),
            ], style=block_style),

            html.Div([
                # Catégorie d'obésité
                html.Label("Métrique", style=label_style),
                dcc.RadioItems(id="q2-metric", value="obesity", inline=True, labelStyle=radio_style,
                               options=[{"label": "Obésité (IMC ≥ 30 kg/m²)", "value": "obesity"},
                                        {"label": "Morbide (IMC ≥ 40 kg/m²)", "value": "morbid"}]),
            ], style={"display": "inline-block", "verticalAlign": "top", "alignItems": "center"}),
        ], style={"marginBottom": "16px", "display": "flex", "flexWrap": "wrap",
                  "justifyContent": "center", "gap": "12px", "alignItems": "center"}),

        dcc.Graph(id="q2-trend", config=graph_config),
    ])




# Callbacks
def register_callbacks(app, df):
    @app.callback(
        Output("q2-trend", "figure"),
        Input("q2-country", "value"),
        Input("q2-country2", "value"),
        Input("q2-sex", "value"),
        Input("q2-metric", "value"))
    def update_figure(country, country2, sex, metric):
        return create_obesity_trend(df, country, country2, sex, metric)
