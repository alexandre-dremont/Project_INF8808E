import dash
from dash import html

from sections.intro_ccl import create_intro, create_conclusion
from sections.section1 import create_section_1
from sections.section2 import create_section_2
from sections.section3 import create_section_3
from sections.section4 import create_section_4

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


# Corps de l'application
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

        # Menu de navigation
        menu_navigation,

        # Titre de l'application
        html.Div(
            className="main",
            children=[
                html.H1("Obésité mondiale :  l'épidémie silencieuse", className="main-title")
            ]
        ),

        # Contenu de l'application
        create_intro(),
        create_section_1(),
        create_section_2(),
        create_section_3(),
        create_section_4(),
        create_conclusion(),          
    ]
)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=True)