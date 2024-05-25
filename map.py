from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

# Load and preprocess the data
df = pd.read_csv('povertydata.csv')
df = df[['Country Name', 'Country Code', 'is_country', 'Income Group', 'GINI index (World Bank estimate)']]
df = df.drop_duplicates(subset=['Country Code', 'Country Name'])

app.layout = html.Div([
    html.H1('Poverty and Equity Database Chloropleth Map'),
    html.Br(),
    dcc.Dropdown(
        id='country_code',
        options=[{'label': country, 'value': code} for code, country in zip(df['Country Code'], df['Country Name'])],
        placeholder='Select a country'
    ),
    dcc.Graph(id='chloropleth')
])

@app.callback(
    Output('chloropleth', 'figure'),
    Input('country_code', 'value')
)
def plot_chloropleth_map(selected_country_code):
    if not selected_country_code:
        return dash.no_update

    filtered_df = df[df['Country Code'] == selected_country_code]

    if filtered_df.empty:
        raise PreventUpdate

    fig = px.choropleth(
        filtered_df,
        locations='Country Code',
        color='GINI index (World Bank estimate)',
        hover_name='Country Code',
        title=f'Choropleth Map for {filtered_df["Country Name"].values[0]}'
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
