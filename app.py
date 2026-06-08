import dash
from dash import html, dcc
import pandas as pd

from components.map import build_layout as build_map, register_callbacks as register_map
from components.bmi_grid import (
    load_country_data,
    build_layout as build_grid,
    register_callbacks as register_grid,
)
from components.timeline import (
    load_ncd_data,
    build_layout as build_timeline,
    register_callbacks as register_timeline,
)
from components.radar_chart import create_radar_chart
from components.stacked_bar_chart import create_stacked_bar_chart_multi
from components.bubble_chart import create_bubble_chart
from components.slope_chart import create_slope_chart, create_multiple_slope_chart


app = dash.Dash(__name__,
                external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap'
])

app.title = 'Project | INF8808'

server = app.server

radar_chart = create_radar_chart()
# stacked_bar_chart = create_stacked_bar_chart_multi()
bubble_chart = create_bubble_chart()
slope_chart = create_multiple_slope_chart()

obesity_df = pd.read_csv("data/obesity_prevalence_world.csv")
country_df = load_country_data()
ncd_df = load_ncd_data()

_hr = html.Hr(style={"margin": "48px 0"})

app.layout = html.Div(
    className="page",
    children=[
        # En-tête
        html.Header(
            className="header",
            children=[
                html.Span("INF8808E - Data Visualization", className="header-title")
            ]
        ),

        # Titre de l'application
        html.Div(
            className="main",
            children=[
                html.H1("Obésité mondiale :  l'épidémie silencieuse", className="main-title")
            ]
        ),

        # Introduction
        html.Div(
            className="introduction",
            children=[
                html.Div(className="section-spliter"),

                html.Div(
                    className="intro-texte",
                    children=[
                        html.P(
                            "D'après l'organisation mondiale de la santé, en 2022, une personne sur huit dans le monde était obèse. Qualifiée d'épidémie, au sens médical du terme, depuis les années 1990, cette pathologie entraîne notamment la diminution de l'espérance de vie, des comorbides parfois graves (sensibilité accrue à la Covid-19 par exemple) ou encore une exposition accrue aux discriminations.",
                            className="intro-paragraphe"
                        ),
                        html.P(
                            "Toujours dans le monde, l'obésité et ses conséquences, qu'elles soient directes ou indirectes, coûtent 2.2% du PIB mondial chaque année. Cette part devrait encore augmenter de moitié d'ici 2060. Il est donc urgent de prendre des mesures efficaces contre le surpoids, l'obésité et ses conséquences délétères aux niveaux individuels et sociétaux.",
                            className="intro-paragraphe"
                        ),
                        html.P(
                            "La vocation de ce panorama visuel est de présenter de manière neutre des données actualisées sur l'obésité, sa prévalence, ses causes et des politiques publiques efficaces pour en juguler la croissance.",
                            className="intro-paragraphe"
                        )
                    ]
                ),

            ]
        ),

        build_map(obesity_df),
        _hr,
        build_grid(country_df),
        _hr,
        build_timeline(ncd_df),
        _hr,

        html.Div(
            className="figure-area",
            children=[
                dcc.Graph(figure=bubble_chart, style={"width": "100%"}),
                dcc.Graph(figure=slope_chart, style={"width": "100%"})
            ]
        ),

        html.Div(
            className="sections",
            children=[
                html.Div(
                    className="section-left",
                    children=[
                        html.Div(
                            className="text-area",
                            children=[
                                html.P("Text explicatif", className="body-sec")
                            ]

                        ),
                        html.Div(
                            className="figure-area",
                            children=[
                                dcc.Graph(figure=radar_chart, style={"width": "100%"}),
                            ]
                        )
                    ]
                )
            ]
        ),

    ]
)

register_map(app, obesity_df)
register_grid(app, country_df)
register_timeline(app, ncd_df)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=True)
