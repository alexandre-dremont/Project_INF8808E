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
                            "D'après l'organisation mondiale de la santé, en 2022, une personne sur huit dans le monde était obèse. Qualifiée d'épidémie, au sens médical du terme, depuis les années 1990, cette pathologie entraîne notamment la diminution de l'espérance de vie, des comorbides parfois graves (sensibilité accrue à la Covid-19 par exemple) ou encore une exposition accrue aux discriminations.",
                            className="intro-paragraphe"
                        ),
                        html.P(
                            "Toujours dans le monde, l'obésité et ses conséquences, qu'elles soient directes ou indirectes, coûtent 2.2% du PIB mondial chaque année. Cette part devrait encore augmenter de moitié d'ici 2060. Il est donc urgent de prendre des mesures efficaces contre le surpoids, l'obésité et ses conséquences délétères aux niveaux individuels et sociétaux.",
                            className="intro-paragraphe"
                        ),
                        html.P(
                            "La vocation de ce panorama visuel est de présenter de manière neutre des données actualisées sur l'obésité, sa prévalence, ses causes et des politiques publiques efficaces pour en juguler la croissance.",
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