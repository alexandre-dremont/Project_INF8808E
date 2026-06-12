import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State, Patch, clientside_callback
from data_preprocessing.dumbbell_data import load_data

# Données 
_df = None

def _get_data():
    global _df
    if _df is None:
        df = load_data()
        df["taux"] = df["cost_2060_usd_ppa"] / df["current_usd_ppa"]
        df = df.sort_values("taux", ascending=True).reset_index(drop=True)
        _df = df
    return _df

def make_figure():
    """
    Construit le dumbell chart orienté (flèché)
    Pour un ensemble de pays, expose le coût croissant, actuel et projeté en 2060, de l"obésité pour la société
    Ce coût est estimé en terme de perte de PIB
    """

    # Chargement des données utiles
    df        = _get_data()
    countries = df["Country"].tolist()
    current   = df["current_usd_ppa"].tolist()
    proj_2060 = df["cost_2060_usd_ppa"].tolist()
    taux      = df["taux"].tolist()
    n         = len(countries)

    # Création d"une figure vièrge
    fig = go.Figure()

    # Vecteur de variation du coût
    for i, (cur, prj) in enumerate(zip(current, proj_2060)):
        fig.add_annotation(
            x=prj-50, y=i, ax=cur+50, ay=i,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.0,
            arrowwidth=1.5, arrowcolor="#4a5568",
            text="")

    # Taux
    for i, (cur, prj, m) in enumerate(zip(current, proj_2060, taux)):
        fig.add_annotation(
            x=(cur + prj) / 2, y=i,
            xref="x", yref="y",
            text=f"×{m:.1f}",
            showarrow=False, yshift=10,
            font=dict(family="Inter, sans-serif", size=9.5, color="#4a5568"),
            bgcolor="rgba(255,255,255,0.72)", borderpad=2)

    # Points actuels
    fig.add_trace(go.Scatter(
        x=current, 
        y=list(range(n)),
        mode="markers",
        name="Coût actuel",
        text=[""] * n, textposition="middle right",
        textfont=dict(family="Inter, sans-serif", size=11, color="#6b8cae"),
        marker=dict(color="#6b8cae", size=11),
        hovertemplate="<b>%{customdata}</b><br>Coût actuel : %{x:,.0f} $ USD PPA/hab.<extra></extra>",
        customdata=countries))

    # Points 2060
    fig.add_trace(go.Scatter(
        x=proj_2060, 
        y=list(range(len(countries))),
        mode="markers+text",
        name="Projection 2060",
        marker=dict(color="#bd4821", size=11),
        text=[""] * n, textposition="middle right",
        textfont=dict(family="Inter, sans serif", size=11, color="#4a5568"),
        hovertemplate="<b>%{customdata}</b><br>Projection 2060 : %{x:,.0f} $ USD PPA/hab.<extra></extra>",
        customdata=countries))

    fig.update_layout(
        # Style de page
        template="plotly_white",
        height=max(400, n*22),
        margin=dict(l=130, r=160, t=20, b=50),

        # Hover
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Axes 
        xaxis=dict(title=dict(text="USD PPA par habitant",
                   font=dict(family="Inter, sans serif", size=11, color="#718096")),
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   ticksuffix=" $",
                   gridcolor="rgba(0,0,0,0.05)"),
        yaxis=dict(tickvals=list(range(len(countries))), 
                   ticktext=countries,
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   ticklabelstandoff=10,
                   gridcolor="rgba(0,0,0,0.05)"),
        
        # Légende
        legend=dict(orientation="h", x=1, y=1,
                    yanchor="bottom", xanchor="right", 
                    font=dict(family="Inter, sans serif", size=12, color="#4a5568"),
                    bgcolor="rgba(0, 0, 0, 0)",
                    borderwidth=0,
                    itemsizing="constant", 
                    traceorder="normal"))
    
    return fig



# Layout 

def make_layout():
    return html.Div([
        dcc.Store(id="dumbbell-visibility", data={"current": True, "proj": True}),
        dcc.Graph(
            id="dumbbell-graph",
            figure=make_figure(),
            style={"width": "100%"},
            config={
                "modeBarButtonsToRemove": [
                    "zoom2d", "pan2d", "zoomIn2d", "zoomOut2d",
                    "autoScale2d", "resetScale2d",
                    "hoverClosestCartesian", "hoverCompareCartesian",
                    "toggleSpikelines", "lasso2d", "select2d"],
                "toImageButtonOptions": {
                    "format": "png", "filename": "dumbbell_chart",
                    "width": 1200, "height": 600, "scale": 2}})])


# Callbacks

def register_callbacks(app):
    clientside_callback(
        """
        function(restyleData, figure) {
            if (!restyleData || !figure) {
                return window.dash_clientside.no_update;
            }
            // Lire l'état réel des traces dans la figure mise à jour par Plotly
            var d = figure.data;
            var visibleVal = function(trace) {
                // Plotly stocke true, false, ou "legendonly"
                var v = trace.visible;
                if (v === undefined || v === true) return true;
                return false;
            };
            return {
                current: visibleVal(d[0]),
                proj:    visibleVal(d[1])
            };
        }
        """,
        Output("dumbbell-visibility", "data"),
        Input("dumbbell-graph", "restyleData"),
        State("dumbbell-graph", "figure"),
        prevent_initial_call=True)

    # Maj flèches, taux et textes des points
    @app.callback(
        Output("dumbbell-graph", "figure"),
        Input("dumbbell-visibility", "data"),
        prevent_initial_call=True)
    def patch_figure(state):
        df        = _get_data()
        n         = len(df)
        current   = df["current_usd_ppa"].tolist()
        proj_2060 = df["cost_2060_usd_ppa"].tolist()

        show_cur  = state.get("current", True)
        show_proj = state.get("proj",    True)
        both      = show_cur and show_proj

        patched = Patch()

        # Texte des points actuels
        patched["data"][0]["mode"] = "markers+text" if (show_cur and not show_proj) else "markers"
        patched["data"][0]["text"] = (
            [f"{v:,.0f} $" for v in current] if (show_cur and not show_proj) else [""] * n)

        # Texte des points 2060
        patched["data"][1]["mode"] = "markers+text" if (show_proj and not show_cur) else "markers"
        patched["data"][1]["text"] = (
            [f"{v:,.0f} $" for v in proj_2060] if (show_proj and not show_cur) else [""] * n)

        # Flèches et taux
        for i in range(n):
            patched["layout"]["annotations"][i]["arrowcolor"] = (
                "#4a5568" if both else "rgba(0,0,0,0)")
            patched["layout"]["annotations"][n + i]["font"] = dict(
                family="Inter, sans-serif", size=9.5,
                color="#4a5568" if both else "rgba(0,0,0,0)")
            patched["layout"]["annotations"][n + i]["bgcolor"] = (
                "rgba(255,255,255,0.72)" if both else "rgba(0,0,0,0)")

        return patched








