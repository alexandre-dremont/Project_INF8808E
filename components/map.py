from dash import dcc, html, Input, Output, State, callback_context, no_update
import pandas as pd
import plotly.graph_objects as go

COLOR_SCALE = "Viridis"
HIGHLIGHT = "#1f78b4"

SEX_PREFIX = {"all": "All_Adults", "male": "Males", "female": "Females"}
SEX_LABEL  = {"all": "Tous adultes", "male": "Hommes", "female": "Femmes"}
MEASURE_LABEL = {"Obesity": "Obésité", "Overweight": "Surpoids"}

DOT_COLORS = {"all": "#636363", "male": "#4292c6", "female": "#d6616b"}


def prepare_data(df):
    """Une ligne par pays : enquête nationale la plus récente."""
    national = df[df["Area"] == "National"].copy()
    national = national.sort_values("Year", ascending=False)
    national = national.drop_duplicates(subset="Country", keep="first")
    return national.reset_index(drop=True)


def value_column(sex, measure):
    return f"{SEX_PREFIX[sex]}_{measure}"


def _hover_frame(dff, col):
    sub = dff.dropna(subset=[col]).copy()
    sub["Income_group"] = sub["Income_group"].fillna("Non classé")
    return sub


def create_choropleth(dff, col, measure, selected):
    sub = _hover_frame(dff, col)
    all_cols = [value_column(sex, measure) for sex in SEX_PREFIX]
    zmax = float(max(dff[c].max() for c in all_cols if c in dff.columns))

    line_width = [2.2 if c == selected else 0.3 for c in sub["Country"]]
    line_color = [HIGHLIGHT if c == selected else "#888888" for c in sub["Country"]]

    fig = go.Figure(
        go.Choropleth(
            locations=sub["Country"],
            locationmode="country names",
            z=sub[col],
            zmin=0,
            zmax=zmax,
            colorscale=COLOR_SCALE,
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
            colorbar=dict(title="%", thickness=12, len=0.7),
        )
    )
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=520,
    )
    return fig


def create_connected_dotplot(dff, measure, selected):
    col_all = value_column("all", measure)
    col_male = value_column("male", measure)
    col_female = value_column("female", measure)

    sub = _hover_frame(dff, col_all).sort_values(col_all, ascending=True).reset_index(drop=True)
    countries = sub["Country"].tolist()

    # Connecting lines: min → max of the 3 values per country
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
        line=dict(color="#cccccc", width=1),
        hoverinfo="skip",
        showlegend=False,
    ))

    if x_sel:
        fig.add_trace(go.Scatter(
            x=x_sel, y=y_sel,
            mode="lines",
            line=dict(color=HIGHLIGHT, width=2.5),
            hoverinfo="skip",
            showlegend=False,
        ))

    for sex, col in [("all", col_all), ("male", col_male), ("female", col_female)]:
        sizes = [10 if c == selected else 7 for c in countries]
        lw = [2 if c == selected else 0 for c in countries]

        fig.add_trace(go.Scatter(
            x=sub[col].values,
            y=sub["Country"].values,
            mode="markers",
            name=SEX_LABEL[sex],
            marker=dict(
                color=DOT_COLORS[sex],
                size=sizes,
                line=dict(width=lw, color="#000000"),
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
        margin=dict(l=10, r=10, t=28, b=30),
        height=max(26 * len(sub), 400),
        xaxis=dict(
            title=f"{MEASURE_LABEL[measure]} (%)",
            range=[0, 100],
            side="top",
            showgrid=True,
            gridcolor="#eee",
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=9),
            range=[-0.3, len(sub) - 0.7],
            categoryorder="array",
            categoryarray=countries,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
        plot_bgcolor="white",
    )
    return fig


def build_layout(df):
    radio_style = {"display": "inline-block", "marginRight": "24px"}
    return html.Div([
        html.H2("Répartition géographique de l'obésité dans le monde"),
        html.P("Comparez les pays sur la carte (vue géographique) et dans le "
               "classement à droite (lecture précise). Cliquez un pays pour le "
               "surligner dans les deux vues."),

        html.Div([
            html.Div([
                html.Label("Carte – Population", style={"fontWeight": "bold", "marginRight": "8px"}),
                dcc.RadioItems(
                    id="sex-toggle",
                    options=[{"label": SEX_LABEL[k], "value": k} for k in ["all", "male", "female"]],
                    value="all",
                    inline=True,
                    labelStyle={"marginRight": "12px"},
                ),
            ], style=radio_style),
            html.Div([
                html.Label("Mesure", style={"fontWeight": "bold", "marginRight": "8px"}),
                dcc.RadioItems(
                    id="measure-toggle",
                    options=[{"label": "Obésité", "value": "Obesity"},
                             {"label": "Surpoids", "value": "Overweight"}],
                    value="Obesity",
                    inline=True,
                    labelStyle={"marginRight": "12px"},
                ),
            ], style=radio_style),
        ], style={"marginBottom": "12px"}),

        html.Div([
            html.Div(
                dcc.Graph(id="obesity-map"),
                style={"flex": "1.5", "position": "sticky", "top": "0",
                       "alignSelf": "flex-start"},
            ),
            html.Div(
                dcc.Graph(id="obesity-dotplot"),
                style={"flex": "1", "maxHeight": "560px", "overflowY": "scroll",
                       "border": "1px solid #eee", "paddingTop": "28px"},
            ),
        ], style={"display": "flex", "gap": "16px", "alignItems": "flex-start"}),

        html.P("Source : World Obesity Federation (2026). "
               "Note : certains territoires (principalement des petites îles du Pacifique et des Caraïbes) "
               "ne figurent pas dans la classification par groupe de revenu de la Banque Mondiale et sont "
               "affichés comme « Non classé ». Les enquêtes datent d'années différentes selon les pays "
               "(indiquée dans l'infobulle). Le classement est trié par prévalence « Tous adultes ».",
               style={"fontSize": "12px", "color": "#666", "marginTop": "8px"}),

        dcc.Store(id="selected-country", data=None),
    ], style={"maxWidth": "1300px", "margin": "0 auto", "fontFamily": "sans-serif"})


def register_callbacks(app, df):
    dff = prepare_data(df)

    @app.callback(
        Output("selected-country", "data"),
        Input("obesity-map", "clickData"),
        Input("obesity-dotplot", "clickData"),
        State("selected-country", "data"),
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
        Input("selected-country", "data"),
    )
    def update_figures(sex, measure, selected):
        col = value_column(sex, measure)
        return (
            create_choropleth(dff, col, measure, selected),
            create_connected_dotplot(dff, measure, selected),
        )
