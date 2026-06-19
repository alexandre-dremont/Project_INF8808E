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
                            "D'après l'Organisation Mondiale de la Santé (OMS), en 2022, une personne sur huit dans le monde était obèse. Qualifiée d'épidémie, au sens médical du terme, depuis les années 1990, cette pathologie présente des impacts sanitaires et économiques croissants à travers l'essentiel des pays du globe.",
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
                html.Div(
                    className="conclusion-texte",
                    children = [
                        html.Div(className="section-splitter"),
                        html.P("En conclusion, à travers ce panorama, nous avons cherché à mettre à disposition de la manière la plus objective possible des données actualisées et fiables sur le surpoids et l'obésité aujourd'hui. Depuis maintenant 50 ans, la prévalence de l'obésité augmente dans le monde entier et aucun pays n'y échappe véritablement. Cette pathologie, souvent considérée comme individuelle et résultant d'une mauvaise hygiène de vie, est en réalité un enjeu de société pour ses impacts nombreux sur notre avenir à tous et ses déterminants aussi nombreux que variés (génétique, inégalités de richesse, sédentarité au travail, etc.). Plutôt que de rejeter la responsabilité de cette maladie sur ceux qui en souffrent, il est nécessaire de considérer ce phénomène comme un tout et apporter une réponse ferme et méthodique contre ceux qui l'alimente pour en limiter les effets délétères. ",
                                className="intro-paragraphe")]
                )
            ]
        )