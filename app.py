import dash
from dash import html


app = dash.Dash(__name__)
app.title = 'Project | INF8808'

app.layout = html.Div([
    html.H1("Voici notre projet de visualisation de données")
])

server = app.server

if __name__ == '__main__':
    app.run(debug=True)