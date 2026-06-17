from dash import html

def create_intro():
    return html.Div(
            className="introduction",
            children=[
                html.Div(className="section-spliter"),

                html.Div(
                    className="intro-texte",
                    children=[
                        html.P(
                            "D'après l'organisation mondiale de la santé, en 2022, une personne sur huit dans le monde était obèse. Qualifiée d'épidémie, au sens médical du terme, depuis les années 1990, cette pathologie présente des impacts sanitaires et économiques croissants à travers l'essentiel des pays du globe.",
                            className="intro-paragraphe"
                        ),
                        html.P(
                            "Toujours dans le monde, l'obésité et ses conséquences, qu'elles soient directes ou indirectes, coûtent l'équivalent de 2.2% du PIB mondial chaque année. Cette part devrait encore augmenter de moitié d'ici 2060 d'après les projections de la Banque Mondiale. Il est donc urgent de mettre en place des actions et d'organiser des politiques publiques pour endiguer ce phénomène.",
                            className="intro-paragraphe"
                        ),
                        html.P(
                            "La vocation de ce panorama visuel est de rendre compte de manière objective des données actualisées sur l'obésité, sa prévalence, ses causes et les politiques publiques envisageables pour en juguler la croissance.",
                            className="intro-paragraphe"
                        )
                    ]
                )
            ]
        )

def create_conclusion():
    return html.Footer(
            className="conclusion",
            children=[
                html.Div(className="section-splitter"),
                html.P(
                    "Ajouter la conclusion",
                    className="intro-paragraphe"
                )
            ]
        )