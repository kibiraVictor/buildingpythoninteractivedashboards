import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import re

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

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
    html.H2('Gini index - World Bank Data',
            style={
                'color': 'blue',
                'fontSize': '40px',
                'textAlign': 'center',
                'fontFamily': 'arial'
            }),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='gini_year_dropdown', options=[{
                'label': year,
                'value': year
            } for year in df['year'].drop_duplicates().sort_values()]),
            dcc.Graph(id='gini_year_barchart')
        ]),
        dbc.Col([
            dcc.Dropdown(id='gini_country_dropdown', options=[{
                'label': country,
                'value': country,
            } for country in df['Country Name'].unique()]),
            dcc.Graph(id='gini_country_barchart')
        ])
    ])
])

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
        plot_bgcolor='white',  # Set background color to black
        paper_bgcolor='white',  # Set paper background color to black
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',  # Faded white grid lines for x-axis
            gridwidth=0.5  # Adjust the width of grid lines
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',  # Faded white grid lines for y-axis
            gridwidth=0.5  # Adjust the width of grid lines
        )
    )
    return fig  # Return the figure

@app.callback(Output('gini_country_barchart', 'figure'),
              Input('gini_country_dropdown', 'value'))
def plot_gini_country_barchart(country, df=df):
    if  not  country :
        return PreventUpdate 
    df1 = df[df['Country Name'] == country]
    fig = px.bar(df1,
                 x='year',
                 y='GINI index (World Bank estimate)',
                 title = 'Country barchart vs GINI')
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
