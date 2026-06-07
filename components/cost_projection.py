import plotly.graph_objects as go
from dash import Dash, dcc, html
from data_preprocessing.roi_data import load_data

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def make_figure():
    df = load_data()

    colors = ['green' if p else 'red' for p in df['profitable']]

    fig = go.Figure(go.Bar(
        x=df['roi'],
        y=df['policy'],
        orientation='h',
        marker_color=colors,
        text=[f'{v:.1f} $' for v in df['roi']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Retour : %{x:.1f} $ par $ investi<extra></extra>',
        width=0.55))

    fig.add_vline(
        x=1.0,
        line=dict(color='orange', width=1.5, dash='dash'),
        annotation_text='Seuil de rentabilité (1 $)',
        annotation_position='top right',
        annotation_font=dict(color='orange', size=10))

    fig.update_layout(
        template='plotly',
        height=380,
        margin=dict(l=230, r=80, t=20, b=50),
        xaxis=dict(title='Retour en USD PPA par dollar investi', ticksuffix=' $',
                   range=[0, df['roi'].max() + 1.2]),
        showlegend=False,
        hovermode='closest')
    return fig

app = Dash(__name__)

app.layout = html.Div([
    html.H4("Rentabilité des politiques publiques de prévention"),
    html.P("Gain en USD PPA pour chaque dollar investi. Au-delà de 1 $, la mesure est rentable. Source : OCDE.",
           style={'color': 'grey', 'fontSize': '12px'}),
    dcc.Graph(figure=make_figure(), config={'displayModeBar': False}),
    html.P("Source : OCDE — Obesity, diet and physical activity",
           style={'color': 'grey', 'fontSize': '11px', 'fontStyle': 'italic'}),
], style={'padding': '20px'})

if __name__ == '__main__':
    app.run(debug=True, port=8051)
