from dash import html, dcc

from components import bubble_chart
from components import slope_chart
from components import heat_map

def create_section_3(slope_df, available_countries):
    """Fonction chargée de créer la section III en HTML.
    Contient les textes et appelle depuis components les visuels de la section III"""
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
                                            html.H2("Des déterminants multiples", className="subtitles")
                                        ]
                                        )
                            ]
                            ),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Les données précédentes permettent de dresser le panorama général de l'obésité dans le monde, sa géographie et son évolution temporelle. Si certaines dynamiques en sont ressorties, il existe cependant une grandes variétés de déterminants de l'obésité dans une population.", className="body-sec"),
                                            html.P("A l'échelle des pays du monde, le premier facteur explicatif de l'obésité auquel il est possible de penser est probablement le lien entre prévalence de l'obésité et niveau de richesse. Ainsi, et de manière assez contre-intuitive, il semble ne pas exister de lien évident entre niveau de richesse d'un pays et prévalence de l'obésité. Il est possible de noter que le quartile des pays les moins riches est en moyenne légèrement moins sujet à la prévalence de l'obésité que les autres groupes de pays mais cette différence reste modeste. Et quand on considère les autres groupes de pays par niveau de richesse, il n'y a plus aucune différence, la richesse d'un pays (en PIB par habitant exprimé en parité de pouvoir d'achat) n'explique pas de manière directe la prévalence de l'obésité dans les pays. Mieux, il ne semble pas exister de lien non plus entre dépenses de santé et prévalence de l'obésité. Ainsi, qu'un pays dépense beaucoup ou peu dans son système de santé n'informe pas sur le taux d'obésité de la population de ce pays. En attestent par exemple la prévalence de l'obésité comparable au Royaume-Uni et en Algérie en 2020 (~31.5%) alors que le premier dépense près de 10 fois plus par an et par habitant dans son système de santé (4.900 US$ contre 490 US$ par an et par hab.). Et les exemples sont nombreux. Il semble donc que les dépenses de santé sont davantage orientées vers les soins curatifs pour les malades que vers les démarches préventives. En outre, il ressort qu'en parallèle de l'augmentation de la prévalence de l'obésité à l'échelle mondiale, les dépenses de santé par habitant ont augmenté dans une large majorité des pays du monde. Si l'obésité n'en est évidemment pas la seule cause, elle est une source de pression supplémentaire sur les systèmes de santé du monde entier, quelle qu'en soit la taille.", className="body-sec"),
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                    # Titre de la figure
                                                    html.H4("Niveau de richesse et dépenses de santé : des facteurs significatifs ?", className="figure-title"),
                                                    # Sous-titre de la figure
                                                    html.H5("Prévalence de l'obésité selon le niveau de richesse et les dépenses de santé des pays en parité de pouvoir d'achat par habitant.", className="figure-subtitle"),
                                                    # Figure
                                                    dcc.Graph(figure=fig_1, style={"width": "100%"}),
                                                    # Ajout des sources et des liens hypertextes
                                                    html.P(children=["Source : ", 
                                                                      html.A("OCDE - Obesity, diet and physical activity",
                                                                             href="https://www.oecd.org/fr/topics/sub-issues/obesity-diet-and-physical-activity.html",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("NCD-RisC (Nature, 2026)",
                                                                        href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    " & ",
                                                                    html.A("Données de la Banque Mondiale",
                                                                             href="https://datacatalog.worldbank.org/",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"})],
                                                                      className="legend"),
                                                ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Mais si le niveau de richesse moyen par habitant ou les dépenses de santé des pays n'expliquent pas la prévalence de l'obésité, d'autres indicateurs culturels, comportementaux et sociétaux parviennent à expliquer, au moins en partie, la tendance à l'augmentation généralisée de la prévalence de l'obésité à travers le monde. Ainsi, l'évolution de l'indice de Gini (mesure standardisée du niveau de partage des richesses au sein d'une population, en l'occurrence au sein de la population de chaque pays ici) est corrélée négativement avec l'évolution de la prévalence de l'obésité dans près de 2 pays sur 3. Un indice de Gini qui augmente signifie un partage de la richesse plus inégalitaire, si Gini vaut 0, tout le monde possède autant et si Gini vaut 1, un seul individu possède tout et les autres rien. Ce que nous apprend cet indicateur, c'est que la moyennisation de la société (tendance au rapprochement de la richesse de la frange la plus pauvre de la population d'un pays avec les \"classes moyennes\") a pu contribuer au développement de l'obésité dans le monde. En effet, la pauvreté extrême disparaissant au profit d'une augmentation du nombre d'individus aux revenus modestes, de nouveaux comportements de consommation émergent. Cette évolution peut-être mise en parallèle au développement d'une alimentation ultra transformée accessible à tous ou à la diversification rapide de l'offre de restauration rapide dans une grande partie du monde. Ce changement dans les habitudes alimentaires est suggéré par la très forte corrélation positive entre variation des apports caloriques quotidiens à travers le monde et prévalence de l'obésité. Depuis 2000, dans plus de 95% des pays du monde, l'apport calorique quotidien à augmenté. Et cette augmentation apparaît comme directement corrélée à l'augmentation de la prévalence de l'obésité dans le monde.", className="body-sec"),
                                            html.P("Finalement, bien qu'elle puisse contribuer à favoriser l'obésité chez l'individu, l'évolution de la sédentarité (et de la pratique sportive par réciprocité) dans une population ne suffit pas à expliquer l'augmentation de la part d'individus en surpoids dans le monde. En effet, dans la moitié des pays du globe, sédentarité de la population et prévalence de l'obésité sont corrélés positivement. Mais dans l'autre moitié des pays du monde, cette corrélation est négative, ce qui indique que des pays qui ont augmenté la part de la population effectuant une activité quotidienne minimale ont tout de même vu la part de population obèse progresser en parallèle.", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     # Titre du visuel 2
                                                    html.H4("L'obésité, une maladie multifactorielle", className="figure-title"),
                                                    # Sous-titre
                                                    html.H5("Corrélation temporelle par pays au cours des dernières décennies de l'évolution des inégalités, de l'apport calorique quotidien ou de la sédentarité avec la prévalence de l'obésité.", className="figure-subtitle"),
                                                    # Figure 2 : Vecteurs de corrléation
                                                    dcc.Graph(figure=fig_2, style={"width": "100%"}),
                                                    # Sources et liens hypertextes
                                                    html.P(children=["Source : ", 
                                                                      html.A("OCDE - Obesity, diet and physical activity",
                                                                             href="https://www.oecd.org/fr/topics/sub-issues/obesity-diet-and-physical-activity.html",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("NCD-RisC (Nature, 2026)",
                                                                        href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("Our World In Data : Diet Composition (2023)",
                                                                        href="https://ourworldindata.org/diet-compositions",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    ", ",
                                                                    html.A("World Health Organisation : Prevalency of insufficient physical activity among adults aged 18+ years (2026)",
                                                                        href="https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-insufficient-physical-activity-among-adults-aged-18-years-(age-standardized-estimate)-(-)",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    " & ",
                                                                    html.A("Données de la Banque Mondiale : Indice de Gini",
                                                                             href="https://datacatalog.worldbank.org/",
                                                                             style={"color": "#A0AEC0", "textDecoration": "none"})],
                                                                      className="legend"),
                                                 ])
                                    ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("Enfin, au-delà de la simple augmentation de l'apport calorique quotidien identifié dans l'écrasante majorité des pays du monde, c'est la composition alimentaire moyenne qui a évoluée. Ainsi, et même si cette règle n'est pas absolue, depuis 1980, c'est l'augmentation de la consommation de sucre, de matières grasses et de produits ultra transformés (contenant des additifs catégorisés \"Autres\" dans le diagramme) qui expliquent l'essentiel de la hausse de l'apport calorique quotidien et qui apparaissent comme les plus corrélés à la prévalence croissante de l'obésité. C'est notamment le cas en France, au Canada, au Brésil, en Corée du Sud ou au Japon pour ne citer qu'eux. En parallèle, la consommation de fruits et légumes n'a pas diminuée, au contraire, elle a même augmenté dans plusieurs pays. Finalement la situation peut se résumer comme suit : le monde consomme les mêmes aliments qu'en 1980 mais avec du sucre, des matières grasses et des additifs en plus.", className="body-sec"),
                                            html.P("L'analyse de tous ces facteurs, qu'ils soient effectivement responsables ou qu'ils soient indépendants de l'évolution de l'obésité dans le monde constituent une base théorique qu'il s'agit de prendre en compte pour orienter les actions et les politiques publiques à mettre en place pour enrayer cette épidémie.", className="body-sec")
                                        ]),
                                        html.Div(className="figure-full",
                                                 children=[
                                                     # Titre du visuel 3
                                                    html.H4("Composition alimentaire et obésité : quels liens ?", className="figure-title"),
                                                    # Sous-titre
                                                    html.H5("Comparaison de l'évolution de l'apport calorique quotidien selon différentes sources alimentaires par rapport à l'obésité. Pour permettre la comparaison, les données sont indexée à 1980, année de références du diagramme.", className="figure-subtitle"),
                                                    # Visuel n°3 : Slope chart composition alimentaire
                                                    slope_chart.create_slope_chart_layout(slope_df, available_countries),
                                                    # Sources et liens hypertextes
                                                    html.P(children=["Source : ", 
                                                                    html.A("Our World In Data : Diet Composition (2023)",
                                                                        href="https://ourworldindata.org/diet-compositions",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"}),
                                                                    " & ",
                                                                    html.A("NCD-RisC (Nature, 2026)",
                                                                        href="https://www.ncdrisc.org/data-downloads-adiposity.html",
                                                                        style={"color": "#a0aec0", "textDecoration": "none"})
                                                    ], className="legend"),
                                                ])
                                    ])
                ]
            )
