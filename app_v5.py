import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import os
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

poverty_data = pd.read_csv('data/PovStatsData.csv')

app.layout = html.Div([
    html.H1('Poverty and Equity Database', style={
        'color': 'blue',
        'fontsize':'40px'
    }),
    html.Br(),
    html.H2('The World Bank'),
    html.Br(),
    dcc.Dropdown(id='country_dropdown', options=[{
        'label': country,
        'value' : country
    } for country in poverty_data['Country Name'].unique()]),
    html.Div(id='report'),
    html.Br(),
    dbc.Tabs([
        dbc.Tab([
            html.Ul([
                html.Li('Number of Economies: 170'),
                html.Li('Temporal Coverages: 1974-2019'),
                html.Li('Last Updated: March 18, 2020'),
                html.Li([
                    'Source: ', html.A('https://datacatalog-world-bank-organisation/poverty-and-equity-database', href='https://datacatalog-world-bank-organisation/poverty-and-equity-database')
                ])
            ])
        ], label='Key Facts'),
        dbc.Tab([
            html.Ul([
                html.Li('Book title: Interactive Dashboards with Dash and Plotly'),
                html.Li('Publisher: PackitPublishers')
            ])
        ], label='Project Info')
    ])

])



@app.callback(Output('report', 'children'),
              Input('country_dropdown', 'value'))
def display_country_report(country):
    if country is None:
        return ''
    
    filtered_df = poverty_data[(
        poverty_data['Country Name'] == country
    ) & (poverty_data['Indicator Name'] == 'Population, total')]
    population = filtered_df.loc[:, '2010'].values[0]
    return [
        html.H3(country),
        f'The population of {country} in 2010 was {population:,.0f}.'
    ]

if __name__ == "__main__":
    app.run_server(debug=True)