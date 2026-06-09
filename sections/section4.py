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
                                                     dcc.Graph(
                                                         figure=fig_1,
                                                         style={"width": "100%"}
                                                     )
                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Ajouter bullet chart et dumbbell chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     dcc.Graph(
                                                         figure=fig_2,
                                                         style={"width": "100%"}
                                                     )
                                                 ])
                                    ])
                ]
            )