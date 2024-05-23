import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

# Connecting to our database
connection_url = "postgresql+psycopg2://root:root@172.18.0.2:5432/povertydb"
engine = create_engine(connection_url, poolclass=NullPool)
engine.connect()

# Define SQL query with filtering
sql_query = """
    SELECT 
    "Country Name", 
    "Indicator Name"
    FROM poverty_data
    WHERE "Indicator Name" = 'Population, total'
    AND "Country Name" IN (SELECT DISTINCT "Country Name" FROM poverty_data)
"""

# Read data directly from SQL
with engine.connect() as connection:
    df = pd.read_sql(sql_query, con=connection)

app.layout = html.Div([
    html.H1('Poverty And Equity Database', style={'color': 'blue', 'fontSize': '40px'}),
    html.Br(),
    dcc.Dropdown(id='country', options=[{'label': country, 'value': country} for country in df['Country Name'].unique()]),
    html.Div(id='report'),
    html.Br(),
    html.H2('The World Bank'),
    html.Br(),
    dbc.Tabs([
        dbc.Tab(label='Key Facts', children=[
            html.Ul([
                html.Li('Number Of Economies: 170'),
                html.Li('Temporal Coverage: 1974-2019'),
                html.Li('Update Frequency: Quarterly'),
                html.Li('Last Updated: March 18, 2020'),
                html.Li([
                    'source: ',
                    html.A('https://datacatalog-worldbank.org/dataset/poverty-and-equity-database',
                           href='https://datacatalog-worldbank.org/dataset/poverty-and-equity-database')
                ])
            ])
        ]),
        dbc.Tab(label='Project Info', children=[
            html.Ul([
                html.Li('Book: Interactve Dashboards Using Dash And Plotly'),
                html.Li('Github repo: Packit Publishing')
            ])
        ])
    ])
])

# Define callback function
@app.callback(Output('report', 'children'), [Input('country', 'value')])
def display_selected_country(country):
    if country is None:
        return ''

    filtered_df = df[df['Country Name'] == country]

    if filtered_df.empty:
        return f"No population data available for {country}"

    population = filtered_df[:].values[0]  # Assuming 'Value' column contains population

    return html.H3(country)

if __name__ == "__main__":
    app.run_server(debug=True)
