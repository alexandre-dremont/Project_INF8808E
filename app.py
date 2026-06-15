import dash
from dash import html
import pandas as pd

from sections.intro_ccl import create_intro, create_conclusion
from sections.section1 import create_section_1
from sections.section2 import create_section_2
from sections.section3 import create_section_3
from sections.section4 import create_section_4

from components.map import register_callbacks as register_map
from components.dumbbell_chart import register_callbacks as register_dumbbell
from components.slope_chart import load_slope_data
from components.slope_chart import register_callbacks as register_slope


from components.bmi_grid import (
    load_country_data,
    register_callbacks as register_grid,
)
from components.timeline import (
    load_ncd_data,
    register_callbacks as register_timeline,
)

# Pré-chargement de données
obesity_df = pd.read_csv("data/obesity_prevalence_world.csv")
country_df = load_country_data()
ncd_df = load_ncd_data()
slope_df, available_countries = load_slope_data()

# Configuration 
app = dash.Dash(__name__, 
                external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap'
])

app.title = 'Project | INF8808'

server = app.server


# Gestion de la navigation dans l'application
menu_navigation = html.Nav(
    className="navigation",
    children=[
        html.A(href="#panorama", className="locker",
               children=[
                   html.Span("I - Panorama mondial", className="locker-survol"),
                   html.Span(className="locker-button")
               ]),               
        html.A(href="#evolution", className="locker",
               children=[
                   html.Span("II - Une évolution contrastée", className="locker-survol"),
                   html.Span(className="locker-button")
               ]), 
        html.A(href="#causes", className="locker",
               children=[
                   html.Span("III - Des determinants multiples", className="locker-survol"),
                   html.Span(className="locker-button")
               ]), 
        html.A(href="#actions", className="locker",
               children=[
                   html.Span("IV - Comment agir efficacement ?", className="locker-survol"),
                   html.Span(className="locker-button")
               ]), 
    ]
)

# Callbacks
register_map(app, obesity_df)
register_grid(app, country_df)
register_timeline(app, ncd_df)
register_slope(app, slope_df, available_countries)
register_dumbbell(app)

# Corps de l'application
app.layout = html.Div(
    className="page",
    children=[
        # Menu de navigation
        menu_navigation,
        html.Div(
            className="variation",
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
                create_intro(),
            ]
        ),
        
        # Contenu de l'application
        create_section_1(obesity_df),
        create_section_2(country_df, ncd_df),
        create_section_3(slope_df, available_countries),
        create_section_4(),
        create_conclusion(),          
    ]
)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=True)
