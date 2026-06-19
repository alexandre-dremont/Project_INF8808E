from dash import html, dcc
from components import cost_projection, dumbbell_chart


def create_section_4():
    fig_2 = cost_projection.make_figure()
    return html.Section(
                id="actions",
                className="sections",
                children=[
                    html.Div(className="section-title",
                            children=[
                                html.Span("IV", className="section-puce"),
                                html.Div(className="hbar"),
                                html.Div(className="section-txt",
                                        children=[
                                            html.P("Politiques publiques et retour sur investissement", className="labels"), 
                                            html.H2("La nécessité d'agir", className="subtitles")
                                        ]
                                        )
                            ]
                            ),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("L'évolution haussière rapide de la prévalence de l'obésité à travers le monde constitue un enjeu auxquels vont être confrontés la quasi totalité des pays du monde, aussi bien d'un point de vue sanitaire et de santé publique qu'en termes économiques et sociaux. Au-delà de dégrader la santé des individus, de les exposer davantage à la discrimination et aux problèmes de santé mentale ou d'accroître le risque de développer des pathologies en marge de l'obésité, les soins à apporter vont entrainer des coûts significatifs pour les systèmes de santé, quels qu'ils soient (augmentation du nombre de praticiens nécessaires, hausse des cotisations sociales, hausse des frais de mutuelle et d'assurance, etc.) et impacter négativement l'économie mondiale (plus d'arrêts maladies, des arrêts plus longs, diminution du ratio actifs/population, etc.). La surcharge pondérale constitue un enjeu de société et mérite des réponses rapides et efficaces dès maintenant pour en limiter les impacts demain.", className="body-sec")
                                        ]),
                                        html.Div(className="text-area", children=[
                                            html.P("Ainsi, selon l'OCDE, si aujourd'hui l'obésité coûte à un mexicain $62 USD PPP/hab., il devrait lui en couter plus de 20 fois plus en 2060. Toujours en 2060 mais aux Etats-Unis cette fois, l'OCDE projette un coût moyen par habitant de l'obésité de $3802 USD PPP/hab. et par an.", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     html.H4("Le coût croissant de le surcharge pondérale", className="figure-title"),
                                                     html.H5("Comparaison des coûts actuels et à l'horizon 2060 de l'obésité selon différents pays", className="figure-subtitle"),
                                                     dumbbell_chart.make_layout(),
                                                     html.P(children=["Sources : ", 
                                                                      html.A("OCDE - Obesity, diet and physical activity",
                                                                             href="https://www.oecd.org/fr/topics/sub-issues/obesity-diet-and-physical-activity.html",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"}),
                                                                      " & ",
                                                                      html.A("Données de la Banque Mondiale",
                                                                             href="https://datacatalog.worldbank.org/",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"})
                                                                    ], 
                                                            className="legend"),
                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Toujours d'après une enquête sur l'obésité menée par l'OCDE, la situation n'est pas désespérée pour autant. Il existe de nombreuses mesures financièrement attractives à condition d'avoir la volonté politique de les mettre en place. Ainsi, pour chaque dollar investi ou perdu en réglementation de la publicité sur les aliments responsables de l'obésité, c'est jusqu'à 5,6$ qui peuvent être économisés à terme pour les systèmes de santé. L'étiquetage des aliments, les programmes de lutte contre la sédentarité, les campagnes de sensibilisation à une hygiène de vie saine ou la mise à disposition d'outils (applications) de suivi de sa santé sont autant de mesures qui peuvent faire la différence. Mieux, cumulées, elles sont d'autant plus efficace. Et même des mesures non directement rentables comme la prescription médicale d'activité physique ou l'allocation d'heures de cours à l'école pour la sensibilisation à la pratique sportive et à une alimentation équilibrée peuvent devenir économiquement intéressantes si on y ajoute les conséquences positives collatérales sur la santé (santé mentale, plus faible risque de développer une maladie, etc.).", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     html.H4("Rentabilité des politiques publiques de prévention de l'obésité", className="figure-title"),
                                                     html.H5("Dans quelles réponses les sociétés doivent-elles investir pour lutter efficacement contre l'obésité ?", className="figure-subtitle"),
                                                     dcc.Graph(figure=fig_2, style={"width": "100%"},
                                                               config={"modeBarButtonsToRemove": ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d",
                                                                            "autoScale2d", "resetScale2d","hoverClosestCartesian", "hoverCompareCartesian",
                                                                            "toggleSpikelines", "lasso2d", "select2d"],
                                                                        "toImageButtonOptions": {"format": "png", "filename": "bar_chart_rdt_mesures",
                                                                            "width": 1200, "height": 500, "scale": 2}}),
                                                     html.P(children=["Source : ", 
                                                                      html.A("OCDE - Obesity, diet and physical activity",
                                                                             href="https://www.oecd.org/fr/topics/sub-issues/obesity-diet-and-physical-activity.html",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"})],
                                                                      className="legend"),
                                                 ])
                                    ])
                ]            )
