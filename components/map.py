from dash import dcc, html, Input, Output, State, callback_context, no_update

from data_preprocessing.obesity_prevalence import obesity_prevalence_most_recent
from components.choropleth_map import create_choropleth
from components.connected_dotplot import create_connected_dotplot


# Layout : carte à gauche et classement défilant (droite). Les jeux de
# boutons et le pays sélectionné dcc.Store pilotent les deux vues.
def build_layout(df):
    label_style = {"fontSize": "11px", "fontWeight": "600", "letterSpacing": "1px",
                   "textTransform": "uppercase", "color": "#6b8cae",
                   "marginRight": "8px", "fontFamily": "Inter, sans serif"}
    radio_style = {"marginRight": "12px", "fontSize": "13px",
                   "color": "#4a5568", "fontFamily": "Inter, sans serif"}

    controls = html.Div([
        html.Div([
            html.Label("Population", style=label_style),
            dcc.RadioItems(id="sex-toggle", value="all", inline=True, labelStyle=radio_style,
                           options=[{"label": "Tous adultes", "value": "all"},
                                    {"label": "Hommes", "value": "male"},
                                    {"label": "Femmes", "value": "female"}]),
        ], style={"display": "inline-flex", "alignItems": "center", "marginRight": "32px"}),
        html.Div([
            html.Label("Mesure", style=label_style),
            dcc.RadioItems(id="measure-toggle", value="Obesity", inline=True, labelStyle=radio_style,
                           options=[{"label": "Obésité", "value": "Obesity"},
                                    {"label": "Surpoids", "value": "Overweight"}]),
        ], style={"display": "inline-flex", "alignItems": "center"}),
    ], style={"marginBottom": "2px"})

    # on retire les outils de zoom de Plotly. Le dot plot ne sert qu'au survol et/ou clic
    dot_config = {
        "modeBarButtonsToRemove": ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
                                   "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian",
                                   "toggleSpikelines", "lasso2d", "select2d"],
        "toImageButtonOptions": {"format": "png", "filename": "prevalence_obesite",
                                 "width": 900, "height": 1200, "scale": 2}}

    return html.Div([
        controls,
        html.Div([
            html.Div(dcc.Graph(id="obesity-map"),
                     style={"flex": "2.6", "position": "sticky", "top": "0",
                            "alignSelf": "flex-start"}),
            html.Div(dcc.Graph(id="obesity-dotplot", config=dot_config),
                     style={"flex": "1", "maxHeight": "375px", "overflowY": "scroll",
                            "paddingTop": "28px"}),
        ], style={"display": "flex", "gap": "16px", "alignItems": "flex-start"}),
        dcc.Store(id="selected-country", data=None),
    ])


# Callbacks
def register_callbacks(app, df):
    dff = obesity_prevalence_most_recent(df)

    # Clic sur une vue ou l'autre sélectionne le pays. Re-cliquer sur le même le désélectionne
    @app.callback(
        Output("selected-country", "data"),
        Input("obesity-map", "clickData"),
        Input("obesity-dotplot", "clickData"),
        State("selected-country", "data"))
    def update_selection(map_click, dot_click, current):
        trigger = callback_context.triggered
        if not trigger:
            return no_update
        source = trigger[0]["prop_id"].split(".")[0]
        click = map_click if source == "obesity-map" else dot_click
        if not click:
            return no_update
        point = click["points"][0]
        country = point.get("location") or point.get("y")  # location = carte, y = dot plot
        return None if country == current else country

    @app.callback(
        Output("obesity-map", "figure"),
        Output("obesity-dotplot", "figure"),
        Input("sex-toggle", "value"),
        Input("measure-toggle", "value"),
        Input("selected-country", "data"))
    def update_figures(sex, measure, selected):
        return (create_choropleth(dff, sex, measure, selected),
                create_connected_dotplot(dff, measure, selected))
