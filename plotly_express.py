import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import re
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.pool import NullPool



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

#creating a connection to my postgres database
connection_url = "postgresql://root:root@172.18.0.2:5432/povertydb"

engine = create_engine(connection_url, poolclass=NullPool)
engine.connect()

#create a connection and close whenever you want to

with engine.connect() as connection:
    try:
       t = text('''
            SELECT * FROM poverty_data
              ''')
       df_sql = pd.read_sql(t, con=engine)
    except Exception as e:
        print('an error occured, seems no connection was found')

# Read the CSV file into a DataFrame
df = pd.read_csv('povertydata.csv')

# Strip leading and trailing whitespaces from column names
df.columns = df.columns.str.strip()

# Select only the desired columns
df = df[['Country Name', 'year', 'GINI index (World Bank estimate)',
         'Income share held by fourth 20%', 'Income share held by highest 20%',
         'Income share held by lowest 20%', 'Income share held by third 20%',
         'Income share held by highest 10%', 'Income share held by lowest 10%',
         'Income share held by second 20%']]

# Drop rows with NaN values in the 'GINI index (World Bank estimate)' column
df = df.dropna(subset=['GINI index (World Bank estimate)'])

# Sort the DataFrame by the 'year' column
df = df.sort_values(by='year')

app.layout = html.Div([
    html.H1('Poverty and Equity Database'),
    html.H2('The World Bank'),
    html.Br(),
    dbc.Tabs([
        dbc.Tab([
            html.Ul([
                html.Li('Number of Economies: 170'),
                html.Li('Temporal Coverage: 1974-2020'),
                html.Li('Update Frequency: Quarterly'),
                html.Li('Last Updated: March 18, 2020'),
                html.Li([
                    'Source: ',
                    html.A('https://datacatalog-worldbank-org/dataset/poverty-and-equity-database', href='https://datacatalog-worldbank-org/dataset/poverty-and-equity-database')
                ])
            ])
        ], label='Key Info'),
        dbc.Tab([
            html.Ul([
                html.Li('Book: Interactive DashBoards with Dash And Plotly'),
                html.Li('Github repo: PackitPublishing')
            ])
        ], label='Project Info')
]), 
    html.Br(),
    # dcc.Dropdown(id='country_dropdwon', options=[{
    #     'label': country,
    #     'value': country
    # } for country in df_sql['Country Name']]),
    # html.Div(id='report'),
    html.Br(),
    #dcc.Graph(id='year_vs_indicator'),
    html.H2('Gini index - World Bank Data',
            style={
                'color': 'black',
                'fontSize': '40px',
                'textAlign': 'center',
                'fontFamily': 'arial'
            }),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='gini_year_dropdown',placeholder='Select a year',options=[{
                'label': year,
                'value': year
            } for year in df['year'].drop_duplicates().sort_values()]),
            dcc.Graph(id='gini_year_barchart')
        ], md=12, lg=5),
        html.Br(),
        dbc.Col([
            dcc.Dropdown(id='gini_country_dropdown',placeholder='Select one or more countries', options=[{
                'label': country,
                'value': country,
            } for country in df['Country Name'].unique()]),
            dcc.Graph(id='gini_country_barchart')
        ], md=12, lg=5)
    ])
   
], style={'backgroundColor': '#E5ECF6'})

# @app.callback(Output('report', 'children'),
#               Input('country_dropdown', 'value'))
# def display_selected_country(country, df_sql=df_sql):
#     if country is None:
#         country = ' You have not selected'
#         return country + 'anything'
#     df_sql = df_sql[df_sql['Country Name'] == country]
#     df_sql=df['Country Name'].unique()
    
# Create year as our callback
@app.callback(Output('gini_year_barchart', 'figure'),
              Input('gini_year_dropdown', 'value'))
def plot_gini_year_barchart(year):
    if year is None:
        raise PreventUpdate
    df_filtered = df[df['year'] == year]  # Use the passed df
    n_countries = len(df_filtered['Country Name'])
    fig = px.bar(df_filtered,  # Use the filtered DataFrame
                 x='GINI index (World Bank estimate)',
                 y='Country Name',
                 orientation='h',
                 height=200 + (n_countries * 20),
                 title='GINI index (World Bank estimate) ' + str(year))
    
    fig.update_layout(
            plot_bgcolor='#E5ECF6',  # Set background color to #E5ECF6
            paper_bgcolor='#E5ECF6',  # Set paper background color to #E5ECF6
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',  # Faded white grid lines for x-axis
                gridwidth=0.5  # Adjust the width of grid lines
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',  # Faded white grid lines for y-axis
                gridwidth=0.5  # Adjust the width of grid lines
            ))
    return fig  # Return the figure

@app.callback(Output('gini_country_barchart', 'figure'),
              Input('gini_country_dropdown', 'value'))
def plot_gini_country_barchart(country, df=df):
    if  not  country :
        return PreventUpdate 
    df1 = df[df['Country Name'] == country]
    fig = px.line(df1,
                 x='year',
                 y='GINI index (World Bank estimate)',
                 title = 'Country barchart vs GINI')
    fig.update_layout(
            plot_bgcolor='#E5ECF6',  # Set background color to #E5ECF6
            paper_bgcolor='#E5ECF6',  # Set paper background color to #E5ECF6
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',  # Faded white grid lines for x-axis
                gridwidth=0.5  # Adjust the width of grid lines
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',  # Faded white grid lines for y-axis
                gridwidth=0.5  # Adjust the width of grid lines
            ))
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
