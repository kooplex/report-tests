from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

import os


URL_PREFIX = os.path.join("/", os.getenv("NB_TESTURL"))
NB_TESTPORT = os.getenv("NB_TESTPORT", 9000)
HOSTNAME = os.getenv("HOSTNAME")
SERVER_NAME = os.getenv("OUTERHOST", 'k8plex-test.vo.elte.hu')

print("You can access your report at %s/%s"%(SERVER_NAME, URL_PREFIX))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], url_base_pathname=URL_PREFIX+"/")

app.layout = html.Div([
    html.H4("Country's key performance analytics"),
    html.P("Select data on y-axis:"),
    dcc.Dropdown(
        id='y-axis',
        options=['lifeExp', 'pop', 'gdpPercap'],
        value='gdpPercap'
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("y-axis", "value"))
def display_area(y):
    df = px.data.gapminder() # replace with your own data source
    countries = (
        df.country.drop_duplicates()
        .sample(n=10, random_state=42)
    )
    df = df[df.country.isin(countries)]

    fig = px.area(
        df, x="year", y=y,
        color="continent", line_group="country")
    return fig

app.run_server(debug=False, port=NB_TESTPORT, host=HOSTNAME)
