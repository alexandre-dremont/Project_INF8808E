import pandas as pd
from dash import html, dcc

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
                                                     build_grid(country_df)
                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Texte stacked area chart", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     build_timeline(ncd_df)
                                                 ])
                                    ]),
                ]
            )