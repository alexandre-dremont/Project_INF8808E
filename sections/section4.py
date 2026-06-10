from dash import html, dcc
from components import cost_projection, dumbbell_chart


def create_section_4():
    fig_1 = dumbbell_chart.make_figure()
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
                                            html.P("Ajouter bullet chart et dumbbell chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     html.H4("Le coût croissant de le surcharge pondérale", className="figure-title"),
                                                     html.H5("Comparaison des coûts actuels et à l'horizon 2060 de l'obésité selon différents pays", className="figure-subtitle"),
                                                     dcc.Graph(figure=fig_1, style={"width": "100%"},
                                                               config={"modeBarButtonsToRemove": ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d",
                                                                            "autoScale2d", "resetScale2d","hoverClosestCartesian", "hoverCompareCartesian",
                                                                            "toggleSpikelines", "lasso2d", "select2d"],
                                                                        "toImageButtonOptions": {"format": "png", "filename": "bar_chart_rdt_mesures",
                                                                            "width": 1200, "height": 500, "scale": 2}}),
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
                                            html.P("Ajouter bullet chart et dumbbell chart", className="body-sec")
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
                                                                             target="_blank",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"})],
                                                                      className="legend"),
                                                 ])
                                    ])
                ]            )