from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash
import pandas as pd
from  sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.pool import NullPool
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash_table

app = dash.Dash( __name__, external_stylesheets=[dbc.themes.COSMO])

postgres_url = "postgresql://root:root@172.18.0.2:5432/povertydb"
engine = create_engine(postgres_url, poolclass=NullPool)
engine.connect()

with engine.connect() as connection:
    t = text(
        '''
        SELECT * FROM poverty_data;
        '''
    )
    df = pd.read_sql(t, con=engine)

app.layout = html.Div([
             html.H1('Hello'),
             dbc.Col([
                 dash_table.DataTable(data=df.to_dict('records'),
                                      columns = [{
                                          'name': col,
                                          'id': col
                                      } for col in df.columns],

                     style_header={'whitespace': 'normal'},
                     fixed_rows={'headers': True},
                     virtualization=True,
                     style_table ={'height': '400px'}
                 )
             ], md=5, lg=7)
])

if __name__ == "__main__":
    try:
        app.run_server(debug=True)
    except PreventUpdate:
        pass  # PreventUpdate exception caught, do nothing