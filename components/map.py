from dash import dcc, html, Input, Output, State, callback_context, no_update
import pandas as pd
import plotly.graph_objects as go

# Les boutons obligent d'utiliser des variables globales 
# Pour donner tous les cas de figure de manière compacte
SEX_PREFIX = {"all": "All_Adults", "male": "Males", "female": "Females"}
SEX_LABEL  = {"all": "Tous adultes", "male": "Hommes", "female": "Femmes"}
MEASURE_LABEL = {"Obesity": "Obésité", "Overweight": "Surpoids"}
DOT_COLORS = {"all": "#636363", "male": "#4292c6", "female": "#d6616b"}


# Pré-traitement des données
def prepare_data(df):
    """Une ligne par pays et enquête nationale la plus récente"""
    national = df[df["Area"] == "National"].copy()
    national = national.sort_values("Year", ascending=False)
    national = national.drop_duplicates(subset="Country", keep="first")
    return national.reset_index(drop=True)


def value_column(sex, measure):
    """Renvoie une chaine de caractère sex_mesure"""
    return f"{SEX_PREFIX[sex]}_{measure}"


def _hover_frame(dff, col):
    sub = dff.dropna(subset=[col]).copy()
    sub["Income_group"] = sub["Income_group"].fillna("Non classé")
    return sub


# Visuel de gauche : carte choroplète
def create_choropleth(dff, col, measure, selected):
    sub = _hover_frame(dff, col)
    all_cols = [value_column(sex, measure) for sex in SEX_PREFIX]
    zmax = float(max(dff[c].max() for c in all_cols if c in dff.columns))

    line_width = [2.2 if c == selected else 0.3 for c in sub["Country"]]
    line_color = ["#2c3e50" if c == selected else "#aaaaaa" for c in sub["Country"]]

    fig = go.Figure(
        go.Choropleth(
            locations=sub["Country"],
            locationmode="country names",
            z=sub[col],
            zmin=0, zmax=zmax,
            colorscale="Ice_r",
            marker_line_color=line_color,
            marker_line_width=line_width,
            customdata=sub[["Income_group", "Year"]],
            hovertemplate=(
                "<b>%{location}</b><br>"
                + f"{MEASURE_LABEL[measure]} : "
                + "%{z:.1f}%<br>"
                "Revenu : %{customdata[0]}<br>"
                "Enquête : %{customdata[1]}<extra></extra>"
            ),
            colorbar=dict(title="%", thickness=12, len=0.6,
                          tickfont=dict(family="Inter, sans serif", size=10, color="#718096")),
        )
    )

    fig.update_layout(
        # Configuration des paramètres géographiques de la carte
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        # Configurations de style
        margin=dict(l=0, r=0, t=10, b=0),
        height=600,
        # Hover
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50"))
    )

    return fig


# Visualisation 2 : Connectd-dot plot
def create_connected_dotplot(dff, measure, selected):
    col_all = value_column("all", measure)
    col_male = value_column("male", measure)
    col_female = value_column("female", measure)

    sub = _hover_frame(dff, col_all).sort_values(col_all, ascending=True).reset_index(drop=True)
    countries = sub["Country"].tolist()

    x_default, y_default = [], []
    x_sel, y_sel = [], []
    for _, row in sub.iterrows():
        vals = [row[c] for c in [col_all, col_male, col_female] if pd.notna(row[c])]
        if len(vals) >= 2:
            seg = [min(vals), max(vals), None]
            if row["Country"] == selected:
                x_sel += seg
                y_sel += [row["Country"], row["Country"], None]
            else:
                x_default += seg
                y_default += [row["Country"], row["Country"], None]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_default, y=y_default,
        mode="lines",
        line=dict(color="#d4dde8", width=1),
        hoverinfo="skip",
        showlegend=False,
    ))

    if x_sel:
        fig.add_trace(go.Scatter(
            x=x_sel, y=y_sel,
            mode="lines",
            line=dict(color="#2c3e50", width=2.5),
            hoverinfo="skip",
            showlegend=False,
        ))

    for sex, col in [("all", col_all), ("male", col_male), ("female", col_female)]:
        
        fig.add_trace(go.Scatter(
            x=sub[col].values,
            y=sub["Country"].values,
            mode="markers",
            name=SEX_LABEL[sex],
            marker=dict(
                color=DOT_COLORS[sex],
                size=[10 if c == selected else 7 for c in countries],
                line=dict(width=[2 if c == selected else 0 for c in countries], color="#2c3e50"),
            ),
            customdata=sub[["Income_group", "Year"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                + f"{MEASURE_LABEL[measure]} – {SEX_LABEL[sex]} : "
                + "%{x:.1f}%<br>"
                "Revenu : %{customdata[0]}<br>"
                "Enquête : %{customdata[1]}<extra></extra>"
            ),
        ))

    fig.update_layout(

        # Style du plot
        margin=dict(l=10, r=10, t=28, b=30),
        height=max(26 * len(sub), 400),
        plot_bgcolor="white",

        # Style de hover
        hoverlabel=dict(bgcolor="white", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),
        
        # Axes 
        xaxis=dict(title=dict(text=f"{MEASURE_LABEL[measure]} (%)",
                              font=dict(family="Inter, sans serif", size=11, color="#718096")),
            tickfont=dict(family="Inter, sans serif", size=10, color="#718096"),
            range=[0, 100],  side="top", showgrid=True, gridcolor="#f0f4f8"),
        yaxis=dict(tickfont=dict(family="Inter, sans serif", size=10, color="#4a5568"),
            showgrid=False, range=[-0.3, len(sub) - 0.7],
            categoryorder="array", categoryarray=countries),

        # Légende
        legend=dict(orientation="h", yanchor="bottom",
            y=1.01, xanchor="center", x=0.5,
            font=dict(family="Inter, sans serif", size=11, color="#4a5568"),
            bgcolor="rgba(0, 0, 0, 0)"
        ),
    )

    return fig


# Construction d'une figure double avec HTML
def build_layout(df):
    label_style = {"fontSize": "11px", "fontWeight": "600", "letterSpacing": "1px",
                   "textTransform": "uppercase", "color": "#6b8cae",
                   "marginRight": "8px", "fontFamily": "Inter, sans serif"}
    radio_style = {"marginRight": "12px", "fontSize": "13px",
                   "color": "#4a5568", "fontFamily": "Inter, sans serif"}
    return html.Div([
            html.Div([
            html.Div([
                html.Label("Population", style=label_style),
                dcc.RadioItems(
                    id="sex-toggle",
                    options=[{"label": SEX_LABEL[k], "value": k} for k in ["all", "male", "female"]],
                    value="all", inline=True,
                    labelStyle=radio_style
                ),
            ], style={"display": "inline-flex", "alignItems": "center", "marginRight": "32px"}),
            html.Div([
                html.Label("Mesure", style=label_style),
                dcc.RadioItems(
                    id="measure-toggle",
                    options=[{"label": "Obésité", "value": "Obesity"},
                             {"label": "Surpoids", "value": "Overweight"}],
                    value="Obesity", inline=True,
                    labelStyle=radio_style
                ),
            ], style={"display": "inline-flex", "alignItems": "center"}),
        ], style={"marginBottom": "16px"}),

        html.Div([
            html.Div(
                dcc.Graph(id="obesity-map"),
                style={"flex": "1.75", "position": "sticky", "top": "0",
                       "alignSelf": "flex-start"},
            ),
            html.Div(
                dcc.Graph(id="obesity-dotplot",
                          config={
                                "modeBarButtonsToRemove": ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d",
                                    "autoScale2d", "resetScale2d", "hoverClosestCartesian", 
                                    "hoverCompareCartesian", "toggleSpikelines", "lasso2d", "select2d"],
                                "toImageButtonOptions": {"format": "png",
                                    "filename": "prevalence_obesite",
                                    "width": 900, "height": 1200,
                                    "scale": 2}
                            }),
                style={"flex": "1", "maxHeight": "560px", "overflowY": "scroll",
                       "paddingTop": "28px"},
            ),
        ], style={"display": "flex", "gap": "16px", "alignItems": "flex-start"}),

        dcc.Store(id="selected-country", data=None)
    ])


# Callbacks pour interactivité
def register_callbacks(app, df):
    dff = prepare_data(df)

    @app.callback(
        Output("selected-country", "data"),
        Input("obesity-map", "clickData"),
        Input("obesity-dotplot", "clickData"),
        State("selected-country", "data")
    )
    def update_selection(map_click, dot_click, current):
        trigger = callback_context.triggered
        if not trigger:
            return no_update
        source = trigger[0]["prop_id"].split(".")[0]
        click = map_click if source == "obesity-map" else dot_click
        if not click:
            return no_update
        point = click["points"][0]
        country = point.get("location") or point.get("y")
        return None if country == current else country

    @app.callback(
        Output("obesity-map", "figure"),
        Output("obesity-dotplot", "figure"),
        Input("sex-toggle", "value"),
        Input("measure-toggle", "value"),
        Input("selected-country", "data")
    )
    def update_figures(sex, measure, selected):
        col = value_column(sex, measure)
        return (
            create_choropleth(dff, col, measure, selected),
            create_connected_dotplot(dff, measure, selected)
        )
