from dash import html, dcc

from components import bubble_chart
from components import slope_chart
from components import heat_map

def create_section_3():
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
                                            html.H2("Des causes multiples", className="subtitles")
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
                                                     dcc.Graph(
                                                         figure=fig_1,
                                                         style={"width": "100%"}
                                                     )
                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Ajouter bubble scatter plot, heatmap et slope chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     dcc.Graph(
                                                         figure=fig_2,
                                                         style={"width": "100%"}
                                                     )
                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Ajouter bubble scatter plot, heatmap et slope chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[slope_chart.create_slope_chart_layout(slope_df, available_countries)]
                                                     )
                                    ])
                ]
            )
