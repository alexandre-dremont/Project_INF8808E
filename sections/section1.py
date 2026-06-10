from dash import html
from components.map import build_layout as build_map


def create_section_1(df):
    return html.Section(
                id="panorama",
                className="sections",
                children=[
                    html.Div(className="section-title",
                            children=[
                                html.Span("I", className="section-puce"),
                                html.Div(className="hbar"),
                                html.Div(className="section-txt",
                                        children=[
                                            html.P("Panorama de l'obésité dans le monde", className="labels"), 
                                            html.H2("Une prévalence globale", className="subtitles")
                                        ])
                            ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Texte carte", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full", children=[
                                            html.P("Répartition géographique de l'obésité dans le monde", className="figure-title"),
                                            html.P("Comparez les pays sur la carte (vue géographique) et dans le classement à droite (lecture précise). Cliquez un pays pour le surligner dans les deux vues.", className="figure-subtitle"),
                                            build_map(df),
                                            html.P(
                                                children=[
                                                    "Sources : ",
                                                    html.A("World Obesity Federation(2026)",
                                                           href="https://data.worldobesity.org/tables/prevalence-of-adult-overweight-obesity-2/",
                                                           style={"color": "#A0AEC0", "textDecoration": "none"}
                                                    )
                                                ], className="legend",
                                            ),
                                            html.P("Note : certains territoires ne figurent pas dans la classification par groupe de revenu de la Banque Mondiale (dénotés «Non classé»). "
                                                    "Les enquêtes datent d'années différentes selon les pays (visible au survol). "
                                                    "Le classement est organisé par prévalence «Tous adultes».", className="notes"),
                                            ])]),
                ]
            )