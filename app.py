import dash
from dash import html, dcc
import pandas as pd

from components.map import create_map


app = dash.Dash(__name__)
app.title = 'Project | INF8808'

server = app.server

df = pd.read_csv("data/obesity_prevalence_world.csv")

map = create_map(df)

app.layout = html.Div([
    html.H1("Voici notre projet de visualisation de données"),
    dcc.Graph(figure=map)
])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=True)