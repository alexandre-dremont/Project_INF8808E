import pandas as pd
from dash import html, dcc

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
                                        ]
                                        )
                            ]
                            ),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Texte carte", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full", children=[build_map(df)])]),
                ]
            )