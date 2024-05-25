import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from dash import html
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

postgres_url = "postgresql://root:root@172.18.0.2:5432/povertydb"
engine = create_engine(postgres_url, poolclass=NullPool)

with engine.connect() as connection:
    r = text('''
        SELECT * FROM poverty_data;
    ''')
    df = pd.read_sql(r, con=engine)

app.layout = html.Div([
    html.Br(),
    html.Div(id='feedback'),
    html.Br(),
    dbc.Label("Create your own dropdown, add options one per line"),
    html.Br(),
    dbc.Textarea(id='Text', cols=40, rows=5),
    html.Br(),
    html.Br(),
    dbc.Button('Set options', id='button'),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id='dropdown', options=[
        {'label': code, 'value': code} for code in df['Country Code'].unique()
    ]),
    html.Br(),
    dcc.Graph(id='chart')
])

# Callback functions
@app.callback(
    [Output('dropdown', 'options'),
     Output('feedback', 'children')],
    [Input('button', 'n_clicks')],
    [State('Text', 'value')]
)
def set_dropdown_options(n_clicks, options):
    if not n_clicks:
        raise PreventUpdate
    text = options.strip().split('\n')
    message = dbc.Alert(f"Success, you added the options: {', '.join(text)}", color='success', dismissable=True)
    options = [{'label': t, 'value': t} for t in text]
    return options, message

@app.callback(
    Output('chart', 'figure'),
    Input('dropdown', 'value')
)
def create_population_chart(country_code):
    if not country_code:
        raise PreventUpdate
    
    with engine.connect() as connection:
        r = text('''
           SELECT * FROM poverty_data
        ''')
        df = pd.read_sql(r, con=engine)

        df = df[df['Country Code'] == country_code]
        df = df[df['Indicator Name'] == 'Population, total']

        fig = px.line(df,
                      x='Indicator Name',
                      y='2010',
                      title=f'Population of {country_code}')
    
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)
