from dash import html
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
                                        ])
                            ]),
                            html.Div(className="section-full",
                                    children=[
                                        html.Div(className="text-area", children=[
                                            html.P("La Fédération Mondiale sur l'Obésité réalise un suivi et documente l'évolution de l'obésité et du surpoids chez l'adulte dans le monde par pays ou région et selon le sexe. Ces données permettent de cartographier la prévalence de l'obésité dans le monde et d'en proposer un panorama mondial actualisé. Bien que certains pays ne communiquent pas de données statistiques consolidées sur la prévalence de l'obésité, principalement en Amérique Latine (Brésil, Colombie, etc.), en Afrique (Egypte, Mali, Afrique du Sud, etc.) ou encore en Asie du Sud-Ouest (Yémen, Pakistan, etc.), il ressort toutefois des tendances géographiques générales. La prévalence de l'obésité apparait comme marquée en Amérique (du Nord comme du Sud), en Australie et en Russie avec des taux d'obésité compris entre 25 et 40% de la population générale. L'Europe, l'Afrique du Nord (Maroc, Algérie, etc.), le Moyen-Orient et l'Asie Centrale forment un groupe où la prévalence de l'obésité apparaît comme intermédiaire (entre 10% et 25% de la population adulte générale). Enfin, l'Afrique subsaharienne et l'Asie Centrale semblent relativement peu touchés par l'obésité avec une prévalence par pays ne dépassant généralement pas 10% de la population adulte. Il est également possible de distinguer un quatrième groupe réunissant les pays insulaires (Samoa, Tonga, Îles Cook, Wallis et Futuna, etc.). Ce dernier groupe, bien que ne représentant pas une grande population à l'échelle mondiale, semblent très fortement touchés par l'obésité avec une prévalence pouvant atteindre plus de 80% de la population adulte de ces pays.", className="body-sec")
                                        ]),
                                        html.Div(className="text-area", children=[
                                            html.P("Ces constats sont révélateurs de déterminants géographiques dans la prévalence de l'obésité, qu'ils soient culturels (alimentaires par exemple), économiques, politiques ou climatiques. Si on prends l'exemple de l'Ethiopie, la prévalence de l'obésité n'y est que de l'ordre de 1% de la population du pays. Cependant, ce pays a longtemps été touché par la famine et la sécurité alimentaire n'y est pas encore garantie pour tous. Il ressort également une forme de séparation entre pays dits du \"Nord global\" et du \"Sud global\" avec des pays du \"Nord\" plus industrialisés et généralement davantage touchés par la surcharge pondérale que les pays du \"Sud\", souvent considérés comme plus pauvres et moins stables politiquement.", className="body-sec")
                                        ]),
                                        
                                        html.Div(className="figure-full", children=[
                                            html.P("Répartition géographique de l'obésité dans le monde", className="figure-title"),
                                            html.P("Comparez les pays sur la carte (vue géographique) et dans le classement à droite (lecture précise). Cliquez un pays pour le surligner dans les deux vues.", className="figure-subtitle"),
                                            build_map(df),
                                            html.P(
                                                children=[
                                                    "Sources : ",
                                                    html.A("World Obesity Federation (2026)",
                                                           href="https://data.worldobesity.org/tables/prevalence-of-adult-overweight-obesity-2/",
                                                           style={"color": "#A0AEC0", "textDecoration": "none"}
                                                    )
                                                ], className="legend",
                                            ),
                                            html.P("Note : certains territoires ne figurent pas dans la classification par groupe de revenu de la Banque Mondiale (dénotés «Non classé»). "
                                                    "Les enquêtes datent d'années différentes selon les pays (visible au survol). "
                                                    "Le classement est organisé par prévalence «Tous adultes».", className="notes"),
                                            ]),
                                            html.Div(className="text-area", children=[
                                                html.P("En outre, il ressort que l'obésité ne touche pas équitablement hommes et femmes selon les pays. Même s'il est admis que les femmes ont une IMC généralement supérieure à celle des hommes, pour des raisons hormonales et métaboliques, ces variations d'IMC entre sexe semblent plus marquées en Afrique, en Asie ou en Amérique du Sud que dans les régions dominées par la culture occidentale comme l'Amérique du Nord, l'Europe ou l'Australie. Ce constat peut trouver une explication dans des normes culturelles et des standards de beauté différents selon les régions ou dans les inégalités de genre dans ces différentes sociétés. Par exemple, dans les sociétés occidentales le corps la femme doit être mince (faible IMC) et le corps de l'homme doit être musclé (IMC élevée). Dans certaines îles du Caraïbéennes, c'est l'inverse qui est jugé comme conforme aux standards de beauté, avec des femmes plus en chair et des hommes plus minces. Enfin, le rôle de la femme au sein de la société peut également contribuer à expliquer des variations de l'obésité entre les sexes, selon que la femme est dans la vie active ou cantonnée à une vie sédentaire au sein du foyer familial.", className="body-sec")
                                            ]),
                                            
                                            ]
                                            ),
                ]
            )