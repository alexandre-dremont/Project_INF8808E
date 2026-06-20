import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc, Input, Output, State, no_update, ctx
from plotly.subplots import make_subplots
from data_preprocessing.dietary_compositions import load_data_dietary_compositions
from data_preprocessing.ncd import load_ncd_risk
from plotly.colors import qualitative

from data_preprocessing.slope_chart_data import (
    filtered_sorted,
    ALL_FOOD_CATEGORIES, CONTINENT_ORDER,
    OBESITY_COL
)

# Nombre de pays affichés par défaut
DEFAULT_NB_COUNTRIES = 12

# Valeurs pour le dropdown pays
SELECT_ALL_VALUE   = "__select_all__"
DESELECT_ALL_VALUE = "__deselect_all__"

def country_options(filtered):
    """Options du dropdown pays avec Tout sélectionner / Tout désélectionner"""
    return ([{"label": f"- Top {DEFAULT_NB_COUNTRIES} pays -",   "value": SELECT_ALL_VALUE},
            {"label": "- Tout désélectionner -", "value": DESELECT_ALL_VALUE}]
        + [{"label": c, "value": c} for c in filtered])

def create_slope_chart_layout(df, available_countries):
    """Retourne le bloc html.Div complet du slope chart avec ses filtres"""

    # Sélection par défaut au chargement
    default_countries  = ["United States of America", "Germany", "Canada", "France", "Brazil", "South Korea", "Senegal", "Japan"]
    default_categories = ["Sucre", "Huiles et graisses", "Autres"]

    # Continents présents dans les données filtrées
    present_continents = set(
        df[df["Entity"].isin(available_countries)]["Continent"].unique())
    
    continent_options = [{"label": "Tous", "value": "Tous"}] + [
        {"label": c, "value": c} for c in CONTINENT_ORDER[1:] 
        if c in present_continents]

    # Styles partagés entre les éléments de contrôle
    label_style = {"fontSize": "11px", "fontWeight": "600", "letterSpacing": "1px",
                   "textTransform": "uppercase", "color": "#6b8cae",
                   "marginRight": "8px", "fontFamily": "Inter, sans serif"}
    
    radio_style = {"marginRight": "12px", "fontSize": "13px",
                   "color": "#4a5568", "fontFamily": "Inter, sans serif"}
    
    block_style = {"display": "inline-block", "marginRight": "28px", "verticalAlign": "top"}

    menu_style  = {"fontSize": "13px", "fontFamily": "Inter, sans serif"}

    # Liste de pays initiale selon le continent et le tri par défaut
    initial_filtered = filtered_sorted(available_countries, df, "Tous", "none")
 
    return html.Div([

        # Filtres
        html.Div([
 
            # Catégories alimentaires
            html.Div([
                html.Label("Catégories alimentaires", style=label_style),
                dcc.Dropdown(
                    id="slope-category-dropdown",
                    options=[{"label": cat, "value": cat} for cat in ALL_FOOD_CATEGORIES],
                    value=default_categories,
                    multi=True,
                    placeholder="Choisir des catégories…",
                    style={**menu_style, "width": "320px"}
                    )
            ], style=block_style),
 
            # Continent
            html.Div([
                html.Label("Continent", style=label_style),
                dcc.Dropdown(
                    id="slope-continent-dropdown",
                    options=continent_options,
                    value="Tous",
                    clearable=False,
                    style={**menu_style, "width": "190px"}
                )
            ], style=block_style),
 
            # Tri
            html.Div([
                html.Label("Trier par variation d'obésité", style=label_style),
                dcc.RadioItems(
                    id="slope-sort",
                    options=[
                        {"label": "Plus forte d'abord", "value": "desc"},
                        {"label": "Plus faible d'abord", "value": "asc"},
                        {"label": "Aucun tri", "value": "none"}],
                    value="none",
                    inline=True,
                    labelStyle=radio_style
                )
            ], style=block_style),
 
            # Pays
            html.Div([
                html.Label("Pays", style=label_style),
                dcc.Dropdown(
                    id="slope-country-dropdown",
                    options=country_options(initial_filtered),
                    value=list(default_countries),
                    multi=True,
                    placeholder="Choisir des pays…",
                    style={**menu_style, "width": "320px"}
                )
            ], style=block_style),
 
        ], style={"marginBottom": "12px", "fontFamily": "Inter, sans serif"}),

        # Graphique principal
        dcc.Graph(
            id="slope-chart-graph",
            figure=create_multiple_slope_chart(df, list(default_countries), default_categories),
            style={"width": "100%"}
        )
 
    ], style={"maxWidth": "1300px", "margin": "0 auto", "fontFamily": "Inter, sans serif"})



# Callbacks
def register_callbacks(app, df, available_countries):
    """Enregistre les callbacks du small multiple slope chart"""
 
    # Mise à jour des options pays selon le continent et le tri choisis
    @app.callback(
        Output("slope-country-dropdown", "options"),
        Input("slope-continent-dropdown", "value"),
        Input("slope-sort", "value"))
    
    def update_country_options(continent, sort):
        filtered = filtered_sorted(available_countries, df, continent, sort)
        return country_options(filtered)
 
    # Mise à jour de la sélection pays
    @app.callback(
        Output("slope-country-dropdown", "value"),
        Input("slope-country-dropdown", "value"),
        Input("slope-continent-dropdown", "value"),
        Input("slope-sort", "value"),
        prevent_initial_call=True)
    def handle_country_value(value, continent, sort):
        from dash import ctx
        filtered = filtered_sorted(available_countries, df, continent, sort)
 
        # Changement de continent ou de tri : reset aux N premiers pays
        if ctx.triggered_id in ("slope-continent-dropdown", "slope-sort"):
            return filtered[:DEFAULT_NB_COUNTRIES]
 
        if not value:
            return []
        if SELECT_ALL_VALUE in value:
            return filtered[:DEFAULT_NB_COUNTRIES]
        if DESELECT_ALL_VALUE in value:
            return []

        # Nettoyage des valeurs sentinelles éventuellement présentes
        return [v for v in value if v not in (SELECT_ALL_VALUE, DESELECT_ALL_VALUE)]
 
    # Mise à jour du graphique selon les pays et catégories sélectionnés
    @app.callback(
        Output("slope-chart-graph", "figure"),
        Input("slope-country-dropdown",  "value"),
        Input("slope-category-dropdown", "value"),
    )
    def update_slope_chart(selected_countries, selected_categories):
        # Filtrage des valeurs sentinelles avant de passer les pays à la figure
        countries = [c for c in (selected_countries or [])
                     if c not in (SELECT_ALL_VALUE, DESELECT_ALL_VALUE)]
        return create_multiple_slope_chart(df, countries, selected_categories or [])


# Construction de la figure
def create_multiple_slope_chart(df, countries, categories):
    """ Construit le small multiple slope chart.
    Pour chaque pays sélectionné, trace l'évolution relative basé en 1980 des
    catégories alimentaires choisies et de la prévalence de l'obésité."""

    # Figure vide par déafut
    if not countries or not categories:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_white",
            annotations=[dict(
                text="Veuillez sélectionner au moins un pays et une catégorie.",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False,
                font=dict(family="Inter, sans serif", size=14, color="#718096"),
            )]
        )
        return fig
 
    years_dietary = sorted(df["Year"].unique())
    all_cols = categories + [OBESITY_COL]

    # Palette de couleurs par catégorie alimentaire
    palette = qualitative.Bold + ["#ddaade"]
    color_map = {cat: palette[i % len(palette)] for i, cat in enumerate(ALL_FOOD_CATEGORIES)}
    color_map[OBESITY_COL] = "#A02B9E"

    # Grille de sous-graphiques avec 4 colonnes maximum
    n_cols = min(len(countries), 4)
    n_rows = -(-len(countries) // n_cols)
 
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=countries, shared_yaxes="all")
    fig.update_annotations(font=dict(family="Inter, sans serif", size=13, color="#4a5568"))
 
    for i, country in enumerate(countries):
        row = i // n_cols + 1
        col = i % n_cols + 1
 
        df_c = df[df["Entity"] == country].sort_values("Year").copy()

        # Référence 1980 
        ref_row = df_c[df_c["Year"] == 1980]
        if ref_row.empty:
            continue
 
        ref_values = ref_row[all_cols].iloc[0]

        # Normalisation
        for col_name in all_cols:
            ref = ref_values[col_name]
            if ref != 0 and pd.notna(ref):
                df_c[col_name] = (df_c[col_name] - ref) / ref
            else:
                df_c[col_name] = float("nan")

        
        # Tracés des catégories alimentaires
        for category in categories:
            fig.add_trace(
                go.Scatter(
                    x=df_c["Year"], y=df_c[category],
                    name=category, mode="lines+markers",
                    line=dict(color=color_map[category]),
                    showlegend=(i == 0),
                    hovertemplate=hover_category(),
                    customdata=[[country, category]] * len(df_c),
                ),
                row=row, col=col,
            )

        # Tracé de la prévalence de l'obésité
        fig.add_trace(
            go.Scatter(
                x=df_c["Year"], y=df_c[OBESITY_COL],
                name="Obésité", mode="lines+markers",
                line=dict(color=color_map[OBESITY_COL], width=3, dash="dot"),
                showlegend=(i == 0),
                hovertemplate=hover_obesity(),
                customdata=[[country]] * len(df_c),
            ),
            row=row, col=col,
        )

    # Ligne de référence 1980 et repères annuels
    fig.add_vline(x=1980, line=dict(color="#E48532", width=2))
    for year in years_dietary:
        fig.add_vline(x=year, line=dict(color="#4E4848", width=1))
 
    # Titre X 
    for idx in range(1, len(countries) + 1):
        axis_key = "xaxis" if idx == 1 else f"xaxis{idx}"
        fig.update_layout(**{axis_key: dict(title=dict(
            text="Année",
            font=dict(family="Inter, sans serif", size=12, color="#718096"),
        ))})

    # Titre Y global
    fig.add_annotation(
        text=f"Variation par rapport à {1980}",
        xref="paper", yref="paper",
        x=-0.08, y=0.5, textangle=-90, showarrow=False,
        font=dict(family="Inter, sans serif", size=13, color="#718096"),
        xanchor="center", yanchor="middle",
    )

    # Mise en page générale
    fig.update_layout(
        # Style de page
        template="plotly_white",
        height=max(300 * n_rows, 300) + 120,
        margin=dict(l=80, b=120),
        # Légende
        legend=dict(
            orientation="h", yanchor="top", y=-120 / (max(300 * n_rows, 300) + 120),
            xanchor="center", x=0.5,
            itemclick=False, itemdoubleclick=False,
            font=dict(family="Inter, sans serif", size=11, color="#2c3e50"),
            bordercolor="#2c3e50", borderwidth=1, bgcolor="#ffffff",
        ),
        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#ffffff", bordercolor="#e2e8f0",
            font=dict(family="Inter, sans serif", size=12, color="#2c3e50"),
        ),
    )

    # Style des axes
    fig.update_xaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
        gridcolor="rgba(0,0,0,0.05)",
    )
    fig.update_yaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
        tickformat=".0%", ticklabelstandoff=10,
    )
 
    return fig


# Template Info-bulles
def hover_category():
    """Génère une info-bulle complète pour les données de chacune des catégories alimentaires"""
    return (
        '<b>%{customdata[0]}</b>'
        "<br>Année : %{x}"
        "<br>Catégorie : %{customdata[1]}"
        "<br>Variation : %{y:.1%}<extra></extra>"
    )
 
def hover_obesity():
    """Génère une info-bulle complète pour les données de prévalence de l'obésité"""
    return (
        '<b>%{customdata[0]}</b>'
        "<br>Année : %{x}"
        "<br>Obésité : %{y:.1%}<extra></extra>"
    )
