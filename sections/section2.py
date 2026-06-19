from dash import html
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
                                            html.P("Au-delà du panorama général de l'obésité aujourd'hui, il est pertinent de se pencher sur l'évolution de la prévalence de l'obésité depuis que cette pathologie est étudiée par la médecine. Des estimations par pays sont disponibles (grâce au groupe de recherche NDC-Risk) depuis 1980 et mettent en évidence des profils d'évolution contrastés mais une tendance commune. En effet, depuis 1980, la prévalence de l'obésité n'a cessé de croître dans la population mondiale. Ainsi, elle a augmenté de 10% passant de 5% de la population mondiale obèse (i.e. avec un indice de masse corporel dépassant le seuil de 30kg/m²) à 15.3% de la population mondiale en 2024. Dans le détail, aucun pays n'est épargné. Sur ce laps de temps, seule la France a vu le taux d'obésité de sa population diminuer marginalement (de l'ordre de -0.1 point de taux d'obésité dans sa population adulte entre 1980 et 2024). Toutefois, la France comme de nombreux pays industrialisés ne brillent pas dans leur gestion du surpoids qui reste relativement élevé en comparaison de pays moins industrialisés d'Afrique, d'Asie ou d'Amérique Latine.", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    html.P("Evolution de la répartition de la population par catégorie d'IMC par pays", className="figure-title"), 
                                                    html.P("Chaque vignette présente l'évolution de la distribution de la population suivant 4 catégories d'IMC, tous les ans, de 1980 à 2024. Le nombre à côté du pays est la variation de l'IMC moyen entre 1980 et 2024 (ex. +3,2). C'est selon ce taux de variation qu'est organisée la grille.", className="figure-subtitle"),
                                                    build_grid(country_df),
                                                    html.P(children=[
                                                        "Source : ", 
                                                        html.A("NCD-Risc (Nature, 2026)", 
                                                                href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                style={"color": "#a0aec0", "textDecoration": "none"})
                                                    ], className="legend"),
                                                    html.P("Note : Estimation standardisées par âge menée sur 200 pays. IMC moyen estimé à partir des milieux de tranche. Les 4 catégories totalisent 100% de la population.", className="notes"),

                                                 ]),
                                        html.Div(className="text-area", children=[
                                            html.P("Par ailleurs, il est possible de distinguer un motif récurrent. Dans les pays comptant le plus faible taux d'obésité au sein de leur population, la prévalence de l'anorexie est très significative. C'est le cas en Erythrée, en Ethiopie ou en Somalie par exemple où la prévalence de l'obésité ne dépasse pas 5% de la population adulte tandis que l'anorexie touche plus de 20% de la population de ces pays. Il existe donc un lien directe entre industrialisation des sociétés et prévalence de l'obésité mais aussi entre disponibilité de la ressource alimentaire et obésité. En particulier, aucun pays ne semble parvenir à éliminer l'insuffisance pondérale tout en jugulant la prévalence de l'obésité.", className="body-sec")
                                            ]),
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Pour comparer encore plus finement l'évolution de de la prévalence de l'obésité entre pays, nous avons développé l'outil suivant :", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    html.P("Prévalence de l'obésité par pays (1980-2024)", className="figure-title"),
                                                    html.P("Le sexe sélectionné apparaît en couleur, encadré de l'intervalle de confiance correspondant à l'estimation du taux d'obésité associé.", className="figure-subtitle"),
                                                    build_timeline(ncd_df),
                                                    html.P(children=[
                                                        "Source : ",
                                                        html.A("NCD-RisC (Nature, 2026)",
                                                            href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                            style={"color": "#a0aec0", "textDecoration": "none"})
                                                    ], className="legend"), 
                                                    html.P("Note : prévalence exprimée en % de la population adulte (≥ 18 ans). L'IMC (Indice de Masse Corporelle) est en kg/m². La bande colorée représente l'intervalle de confiance à 95 %. «Tous adultes» = moyenne Hommes/Femmes.", className="notes")
                                                 ]),
                                            html.Div(className="text-area", children=[
                                                html.P("Prenons l'exemple particulier des Etats-Unis (United States of America) et de la Chine (China). Les deux pays peuvent aujourd'hui être considérés comme industrialisés, le premier depuis maintenant plusieurs décennies et le second depuis quelques années au moins. On constate alors deux évolutions contrastées. D'une part, les USA semblent atteindre un plateau dans l'augmentation de la prévalence de l'obésité, ou au moins un ralentissement notable depuis 2010 environ. D'autre part, la Chine compte quant à elle une part exponentiellement croissante d'obésité au sein de sa population. Les taux de prévalence des deux pays ne sont absolument pas comparables, au même titre que leur culture alimentaire et sportive, leur rapport au surpoids ou leur histoire. Toutefois, le phénomène d'industrialisation de l'alimentation semble directement corrélé à l'augmentation de la prévalence de l'obésité.", className="body-sec")
                                            ]),
                                            html.Div(className="text-area", children=[
                                                html.P("Un autre exemple riche d'enseignements est la comparaison entre l'évolution du taux d'obésité par sexe en Allemagne (Germany) et au Sénégal (Senegal). Dans la population adulte générale, l'Allemagne présente un taux d'obésité presque deux fois supérieur à celui du Sénégal mais celui du Sénégal augmente rapidement tandis qu'en Allemagne, l'obésité est stable. Pourtant la prévalence de l'obésité chez les femmes dans ces deux pays est aujourd'hui presque identique, tandis que la prévalence de l'obésité chez les hommes est de l'ordre de quatre fois supérieur en Allemagne par rapport au Sénégal. Comme évoqué plus tôt, cette tendance relève davantage de la culture et des standards de beauté régionaux que de facteurs économiques ou d'accès à l'alimentation. L'Allemagne est un pays européen au profil occidental, valorisant la minceur chez les femmes et la carrure large chez les hommes. Au contraire, au Sénégal, il est vu comme un signe de bonne santé que les femmes soient plus corpulentes tandis que les hommes sont plus enclins à la maigreur.", className="body-sec")
                                            ]),
                                    ]),
                ]
            )