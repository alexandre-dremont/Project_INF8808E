import dash
from dash import html, dcc
import pandas as pd

from components.map import create_map


app = dash.Dash(__name__, 
                external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap'
])

app.title = 'Project | INF8808'

server = app.server

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
        )

        # Ajouter le contenu des sctions ici

    ]
)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=True)