import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

connection_url = "postgresql+psycopg2://root:root@172.18.0.2:5432/povertydb"

engine = create_engine(connection_url, poolclass=NullPool)

with engine.connect() as connection:
    t = text('SELECT * FROM poverty_data')
    df = pd.read_sql(t, con=engine)

regions = ['East Asia & Pacific', 'Europe & Central Asia', 'Fragile and conflict affected situations', 'High income',
           'IDA countries classified as fragile situations', 'IDA total', 'Latin America & Caribbean', 'Low & middle income', 'Low income', 'Lower middle income', 'Middle East & North Africa', 'Middle income', 'South Asia',
           'Sub-Saharan Africa', 'Upper middle income', 'World']

population_df = df[~df['Country Name'].isin(regions) & (df['Indicator Name'] == 'Population, total')]

app.layout = html.Div([
    html.H1('Poverty And Equity Database'),
    html.Br(),

    dcc.Dropdown(id='year_dropdown',
                 options=[{'label': str(year), 'value': str(year)} for year in range(1974, 2020)],
                 placeholder="Select a year"),
    dcc.Graph(id='population_chart')
])

@app.callback(Output('population_chart', 'figure'),
              Input('year_dropdown', 'value'))
def plot_countries_by_population(year):
    fig = go.Figure()

    # Check if the year is valid
    if year is None or year not in population_df.columns:
        fig.layout.title = 'Please select a valid year from the dropdown.'
        return fig

    year_df = population_df[['Country Name', year]].sort_values(year, ascending=False).head(20)
    fig.add_bar(x=year_df['Country Name'], y=year_df[year])
    fig.layout.title = f'Top twenty countries by population - {year}'
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
