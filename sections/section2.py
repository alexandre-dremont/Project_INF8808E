from dash import html
from components.bmi_grid import build_layout as build_grid
from components.timeline import build_layout as build_timeline


def create_section_2(country_df, ncd_df):
    return html.Section(
                id="evolution",
                className="sections",
                children=[
                    html.Div(className="section-title",
                            children=[
                                html.Span("II", className="section-puce"),
                                html.Div(className="hbar"),
                                html.Div(className="section-txt",
                                        children=[
                                            html.P("Evolution temporelle par pays", className="labels"), 
                                            html.H2("Une évolution contrastée", className="subtitles")
                                        ]
                                        )
                            ]
                            ),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Texte stacked area chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    html.P("Evolution de la répartition de la population par catégorie d'IMC par pays", className="figure-title"), 
                                                    html.P("Chaque vignette présente l'évolution de la distribution de la population suivant 4 catégories d'IMC, tous les ans, de 1980 à 2024. Le nombre à côté du pays est la variation de l'IMC moyen entre 1980 et 2024 (ex. +3,2). C'est selon ce taux de variation qu'est organisée la grille.", className="figure-subtitle"),
                                                    build_grid(country_df),
                                                    html.P(children=[
                                                        "Source : ", 
                                                        html.A("NCD-Risc (Nature, 2026)", 
                                                                href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                style={"color": "#a0aec0", "textDecoration": "none"})
                                                    ], className="legend"),
                                                    html.P("Note : Estimation standardisées par âge menée sur 200 pays. IMC moyen estimé à partir des milieux de tranche. Les 4 catégories totalisent 100% de la population.", className="notes")

                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Texte stacked area chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    html.P("Prévalence de l'obésité par pays (1980-2024)", className="figure-title"),
                                                    html.P("Le sexe sélectionné apparaît en couleur, encadré de l'intervalle de confiance correspondant à l'estimation du taux d'obésité associé.", className="figure-subtitle"),
                                                    build_timeline(ncd_df),
                                                    html.P(children=[
                                                        "Source : ",
                                                        html.A("NCD-RisC (Nature, 2026)",
                                                            href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                            style={"color": "#a0aec0", "textDecoration": "none"})
                                                    ], className="legend"), 
                                                    html.P("Note : prévalence exprimée en % de la population adulte (≥ 18 ans). L'IMC (Indice de Masse Corporelle) est en kg/m². La bande colorée représente l'intervalle de confiance à 95 %. «Tous adultes» = moyenne Hommes/Femmes.", className="notes")
                                                 ])
                                    ]),
                ]
            )