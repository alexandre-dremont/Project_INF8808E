from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go

COUNTRY_FILE = "data/NCD_RisC_Nature_2026_BMI_age_standardised_country.csv"
WORLD_FILE   = "data/NCD_RisC_Nature_2026_BMI_age_standardised_world.csv"

SEX_LABEL = {"Men": "Hommes", "Women": "Femmes", "All": "Tous adultes"}

OBESITY = ("Prevalence of BMI>=30 kg/m² (obesity)",        "Obésité (IMC ≥ 30 kg/m²)",        "solid")
MORBID  = ("Prevalence of BMI >=40 kg/m² (morbid obesity)", "Obésité morbide (IMC ≥ 40 kg/m²)", "dot")

# --- encodage couleur mode simple ---
ALL_COLOR = "#333333"
ALL_BAND  = "rgba(51,51,51,0.10)"
# Sexe : couleurs sémantiques universelles
SEX_COLORS = {
    "Men":   {"active": "#1565c0", "band": "rgba(21,101,192,0.13)",
              "inactive": "rgba(21,101,192,0.28)"},
    "Women": {"active": "#c2185b", "band": "rgba(194,24,91,0.13)",
              "inactive": "rgba(194,24,91,0.28)"},
}

COUNTRY_STYLES = ["solid", "dash"]   # pays 1 = trait continu, pays 2 = pointillés

NO_COUNTRY = "__none__"


def _display_name(country):
    return "Monde" if country == "World" else country


def load_ncd_data():
    frames = []
    for path in [WORLD_FILE, COUNTRY_FILE]:
        d = pd.read_csv(path)
        d.columns = [c.strip().lstrip("﻿") for c in d.columns]
        d = d.rename(columns={"Country/Region/World": "Country"})
        frames.append(d)
    return pd.concat(frames, ignore_index=True)


def _filter(df, country, sex):
    return df[(df["Country"] == country) & (df["Sex"] == sex)].sort_values("Year")


def _all_adults(df, country):
    sub = df[df["Country"] == country]
    num_cols = [c for c in sub.select_dtypes("number").columns if c != "Year"]
    avg = sub.groupby("Year")[num_cols].mean().reset_index()
    avg["Country"] = country
    return avg


def _add_ci(fig, dff, base, band_color):
    lo = base + " lower 95% uncertainty interval"
    hi = base + " upper 95% uncertainty interval"
    if lo not in dff.columns or hi not in dff.columns:
        return
    fig.add_trace(go.Scatter(
        x=dff["Year"], y=dff[hi] * 100, mode="lines",
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=dff["Year"], y=dff[lo] * 100, mode="lines",
        line=dict(width=0), fill="tonexty", fillcolor=band_color,
        showlegend=False, hoverinfo="skip",
    ))


def _add_line(fig, dff, base, name, color, dash, width=2.0, opacity=1.0):
    fig.add_trace(go.Scatter(
        x=dff["Year"], y=dff[base] * 100, mode="lines",
        line=dict(width=width, color=color, dash=dash),
        opacity=opacity, name=name,
        hovertemplate=f"{name}<br>%{{x}} : %{{y:.1f}} %<extra></extra>",
    ))


def _draw_country(fig, df, country, selected_sex, series, line_style=None, label_prefix=""):
    prefix = f"{label_prefix} — " if label_prefix else ""

    if selected_sex == "All":
        dff = _all_adults(df, country)
        for base, label, dash in series:
            d = line_style if line_style else dash
            _add_ci(fig, dff, base, ALL_BAND)
            _add_line(fig, dff, base, f"{prefix}{label} — Tous adultes",
                      ALL_COLOR, d, width=2.3)
        return dff

    other_sex  = "Women" if selected_sex == "Men" else "Men"
    dff_active = _filter(df, country, selected_sex)
    dff_other  = _filter(df, country, other_sex)

    c_active   = SEX_COLORS[selected_sex]["active"]
    b_active   = SEX_COLORS[selected_sex]["band"]
    c_inactive = SEX_COLORS[other_sex]["inactive"]

    for base, label, dash in series:
        d = line_style if line_style else dash
        _add_line(fig, dff_other, base,
                  f"{prefix}{label} — {SEX_LABEL[other_sex]}",
                  c_inactive, d, width=1.3)
        _add_ci(fig, dff_active, base, b_active)
        _add_line(fig, dff_active, base,
                  f"{prefix}{label} — {SEX_LABEL[selected_sex]}",
                  c_active, d, width=2.0)

    return dff_active


def create_obesity_trend(df, country1, country2, selected_sex, metric):
    series    = [MORBID] if metric == "morbid" else [OBESITY]
    comparing = country2 and country2 != NO_COUNTRY
    fig       = go.Figure()

    if comparing:
        ann_color = (ALL_COLOR if selected_sex == "All"
                     else SEX_COLORS[selected_sex]["active"])
        for country, line_style in zip([country1, country2], COUNTRY_STYLES):
            dff = _draw_country(fig, df, country, selected_sex, series,
                                line_style, label_prefix=_display_name(country))
            last = dff[dff["Year"] == dff["Year"].max()]
            if not last.empty:
                y_val = last[series[0][0]].iloc[0] * 100
                fig.add_annotation(
                    x=2024, y=y_val,
                    text=f"<b>{_display_name(country)}</b>",
                    xanchor="left", yanchor="middle",
                    showarrow=False, xshift=6,
                    font=dict(size=10, color=ann_color),
                )
        title = (f"Obésité — {_display_name(country1)} vs {_display_name(country2)}"
                 f"  ({SEX_LABEL[selected_sex]} mis en évidence)")
    else:
        _draw_country(fig, df, country1, selected_sex, series)
        title = (f"Prévalence de l'obésité — {_display_name(country1)}"
                 f"  ({SEX_LABEL[selected_sex]} mis en évidence)")

    fig.update_layout(
        title=title,
        xaxis=dict(title="Année", range=[1980, 2030],
                   tickvals=[1980, 1990, 2000, 2010, 2020, 2024]),
        yaxis=dict(title="Part de la population", rangemode="tozero", ticksuffix=" %"),
        legend=dict(font=dict(size=10)),
        hovermode="x unified", plot_bgcolor="white",
        margin=dict(l=60, r=80, t=50, b=40), height=420,
    )
    return fig


def build_layout(df):
    countries = sorted(df["Country"].unique())
    if "World" in countries:
        countries = ["World"] + [c for c in countries if c != "World"]
    options = [{"label": _display_name(c), "value": c} for c in countries]
    compare_options = [{"label": "— aucun —", "value": NO_COUNTRY}] + options

    return html.Div([
        html.H2("Évolution de la prévalence de l'obésité (1980–2024)"),
        html.P("Le sexe sélectionné apparaît en couleur, l'autre en grisé. "
               "La courbe épaisse représente tous les adultes."),

        html.Div([
            html.Div([
                html.Label("Pays", style={"fontWeight": "bold", "fontSize": "15px", "marginRight": "8px"}),
                dcc.Dropdown(id="q2-country", options=options,
                             value="World", clearable=False, searchable=True,
                             style={"width": "190px"}),
            ], style={"display": "inline-block", "marginRight": "24px", "verticalAlign": "top"}),

            html.Div([
                html.Label("Comparer avec", style={"fontWeight": "bold", "fontSize": "15px", "marginRight": "8px"}),
                dcc.Dropdown(id="q2-country2", options=compare_options,
                             value=NO_COUNTRY, clearable=False, searchable=True,
                             style={"width": "190px"}),
            ], style={"display": "inline-block", "marginRight": "24px", "verticalAlign": "top"}),

            html.Div([
                html.Label("Sexe", style={"fontWeight": "bold", "fontSize": "15px", "marginRight": "8px"}),
                dcc.RadioItems(
                    id="q2-sex",
                    options=[{"label": SEX_LABEL[k], "value": k}
                             for k in ["Men", "Women", "All"]],
                    value="Men", inline=True,
                    labelStyle={"marginRight": "10px", "fontSize": "15px"},
                ),
            ], style={"display": "inline-block", "marginRight": "24px", "verticalAlign": "top"}),

            html.Div([
                html.Label("Métrique", style={"fontWeight": "bold", "fontSize": "15px", "marginRight": "8px"}),
                dcc.RadioItems(
                    id="q2-metric",
                    options=[
                        {"label": "Obésité (IMC ≥ 30 kg/m²)", "value": "obesity"},
                        {"label": "Morbide (IMC ≥ 40 kg/m²)",  "value": "morbid"},
                    ],
                    value="obesity", inline=True,
                    labelStyle={"marginRight": "10px", "fontSize": "15px"},
                ),
            ], style={"display": "inline-block", "verticalAlign": "top"}),
        ], style={"marginBottom": "12px"}),

        dcc.Graph(id="q2-trend"),

        html.P(
            "Note : prévalence exprimée en % de la population adulte (≥ 18 ans). "
            "L'IMC (Indice de Masse Corporelle) est en kg/m². "
            "La bande colorée représente l'intervalle de confiance à 95 %. "
            "« Tous adultes » = moyenne Hommes/Femmes.",
            style={"fontSize": "12px", "color": "#666", "marginTop": "8px"}),
        html.P(
            "Source : NCD-RisC (Nature, 2026) — estimations statistiques standardisées par âge.",
            style={"fontSize": "12px", "color": "#666", "marginTop": "2px"}),
    ], style={"maxWidth": "1300px", "margin": "0 auto", "fontFamily": "sans-serif"})


def register_callbacks(app, df):
    @app.callback(
        Output("q2-trend", "figure"),
        Input("q2-country", "value"),
        Input("q2-country2", "value"),
        Input("q2-sex", "value"),
        Input("q2-metric", "value"),
    )
    def update_figure(country, country2, sex, metric):
        return create_obesity_trend(df, country, country2, sex, metric)
