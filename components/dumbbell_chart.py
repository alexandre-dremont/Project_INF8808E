import plotly.graph_objects as go
from dash import Dash, dcc, html
from data_preprocessing.dumbbell_data import load_data

def make_figure():
    df = load_data()
    countries = df['Country'].tolist()
    current   = df['current_usd_ppa'].tolist()
    proj_2060 = df['cost_2060_usd_ppa'].tolist()

    fig = go.Figure()

    # Lignes de connexion grises
    for i, (cur, prj) in enumerate(zip(current, proj_2060)):
        fig.add_shape(
            type='line', x0=cur, x1=prj, y0=i, y1=i,
            line=dict(color='lightgrey', width=1.5))
        fig.add_annotation(
            x=prj - 55, y=i, ax=cur + 55, ay=i,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1.0,
            arrowwidth=1.5, arrowcolor='grey',
            text='')

    # Points actuels
    fig.add_trace(go.Scatter(
        x=current, y=list(range(len(countries))),
        mode='markers',
        name='Dépenses actuelles',
        marker=dict(color='grey', size=12),
        hovertemplate='<b>%{customdata}</b><br>Dépenses actuelles : %{x:,.0f} $ USD PPA/hab.<extra></extra>',
        customdata=countries))

    # Points 2060
    fig.add_trace(go.Scatter(
        x=proj_2060, y=list(range(len(countries))),
        mode='markers+text',
        name='Projection 2060',
        marker=dict(color='red', size=14),
        text=[f'{v:,.0f} $' for v in proj_2060],
        textposition='middle right',
        hovertemplate='<b>%{customdata}</b><br>Projection 2060 : %{x:,.0f} $ USD PPA/hab.<extra></extra>',
        customdata=countries))

    fig.update_layout(
        template='plotly',
        height=400,
        margin=dict(l=130, r=160, t=20, b=50),
        xaxis_title='USD PPA par habitant',
        yaxis=dict(tickvals=list(range(len(countries))), ticktext=countries),
        legend=dict(orientation='h', x=0, y=1.08),
        hovermode='closest')
    return fig

app = Dash(__name__)

app.layout = html.Div([
    html.H4("Coût économique de l'obésité : dépenses actuelles vs projection 2060"),
    html.P("Dépenses actuelles (USD PPA/hab.) vs coût projeté en 2060. Source : OCDE, Banque Mondiale.",
           style={'color': 'grey', 'fontSize': '12px'}),
    dcc.Graph(figure=make_figure(), config={'displayModeBar': False}),
    html.P("Sources : OCDE | Banque Mondiale (2023)",
           style={'color': 'grey', 'fontSize': '11px', 'fontStyle': 'italic'}),
], style={'padding': '20px'})

if __name__ == '__main__':
    app.run(debug=True)
