from dash import html, dcc

from components import bubble_chart
from components import slope_chart
from components import heat_map

def create_section_3(slope_df, available_countries):
    fig_1 = bubble_chart.create_bubble_chart()
    fig_2 = heat_map.create_heat_map()

    return html.Section(
                id="causes",
                className="sections",
                children=[
                    html.Div(className="section-title",
                            children=[
                                html.Span("III", className="section-puce"),
                                html.Div(className="hbar"),
                                html.Div(className="section-txt",
                                        children=[
                                            html.P("Facteurs explicatifs", className="labels"), 
                                            html.H2("Des déterminants multiples", className="subtitles")
                                        ]
                                        )
                            ]
                            ),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Ajouter bubble scatter plot, heatmap et slope chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    html.H4("Niveau de richesse et dépenses de santé : des facteurs significatifs ?", className="figure-title"),
                                                    html.H5("Prévalence de l'obésité selon le niveau de richesse et les dépenses de santé des pays en parité de pouvoir d'achat par habitant.", className="figure-subtitle"),
                                                    dcc.Graph(figure=fig_1, style={"width": "100%"}),
                                                    html.P(children=["Source : ", 
                                                                      html.A("OCDE - Obesity, diet and physical activity",
                                                                             href="https://www.oecd.org/fr/topics/sub-issues/obesity-diet-and-physical-activity.html",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("NCD-RisC (Nature, 2026)",
                                                                        href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    " & ",
                                                                    html.A("Données de la Banque Mondiale",
                                                                             href="https://datacatalog.worldbank.org/",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"})],
                                                                      className="legend"),
                                                ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Ajouter bubble scatter plot, heatmap et slope chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    html.H4("L'obésité, une maladie multifactorielle", className="figure-title"),
                                                    html.H5("Corrélation temporelle par pays au cours des dernières décennies de l'évolution des inégalités, de l'apport calorique quotidien ou de la sédentarité avec la prévalence de l'obésité.", className="figure-subtitle"),
                                                    dcc.Graph(figure=fig_2, style={"width": "100%"}),
                                                    html.P(children=["Source : ", 
                                                                      html.A("OCDE - Obesity, diet and physical activity",
                                                                             href="https://www.oecd.org/fr/topics/sub-issues/obesity-diet-and-physical-activity.html",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("NCD-RisC (Nature, 2026)",
                                                                        href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("Our World In Data : Diet Composition (2023)",
                                                                        href="https://ourworldindata.org/diet-compositions",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("World Health Organisation : Prevalency of insufficient physical activity among adults aged 18+ years (2026)",
                                                                        href="https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-insufficient-physical-activity-among-adults-aged-18-years-(age-standardized-estimate)-(-)",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    " & ",
                                                                    html.A("Données de la Banque Mondiale : Indice de Gini",
                                                                             href="https://datacatalog.worldbank.org/",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"})],
                                                                      className="legend"),
                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Ajouter bubble scatter plot, heatmap et slope chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    html.H4("Composition alimentaire et obésité : quels liens ?", className="figure-title"),
                                                    html.H5("Comparaison de l'évolution de l'apport calorique quotidien selon différentes sources alimentaires par rapport à l'obésité. Pour permettre la comparaison, les données sont indexée à 1980, année de références du diagramme.", className="figure-subtitle"),
                                                    slope_chart.create_slope_chart_layout(slope_df, available_countries),
                                                    html.P(children=["Source : ", 
                                                                    html.A("Our World In Data : Diet Composition (2023)",
                                                                        href="https://ourworldindata.org/diet-compositions",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    " & ",
                                                                    html.A("NCD-RisC (Nature, 2026)",
                                                                        href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"})
                                                    ], className="legend"),
                                                ])
                                    ])
                ]
            )
