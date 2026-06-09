from dash import html

def create_section_2():
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
                                        # Ajouter la carte ici
                                    ])
                ]
            )