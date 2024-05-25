from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

postgres_url = "postgresql://root:root@172.18.0.2:5432/povertydb"

engine = create_engine(postgres_url, poolclass=NullPool)

with engine.connect() as connection:
    t = text('''
        SELECT DISTINCT "Country Code" FROM poverty_data;
    ''')
    df = pd.read_sql(t, con=connection)

app.layout = html.Div([
    html.H1('Choropleth and scattermapbox',
            style={
                'color': 'blue',
                'textAlign': 'center',
                'fontSize': '25px'
            }),
    html.Br(),
    dcc.Dropdown(
        id='country-code',
        options=[{'label': code, 'value': code} for code in df['Country Code']],
        placeholder='Select a country'
    ),
    dcc.Graph(id='mapplot')
])

@app.callback(Output('mapplot', 'figure'), [Input('country-code', 'value')])
def plot_map_scatter_plot(code):
    if not code:
        raise PreventUpdate

    with engine.connect() as connection:
        t = text('''
            SELECT "Country Code", "Country Name", "Indicator Name"
            FROM poverty_data;
        ''')
        
        country_df =pd.read_sql(t, con=engine)

    fig = px.choropleth(
        country_df,
        locations='Country Code',
        hover_name='Country Name',
        color='Country Name',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
