import dash
import pandas as pd
import plotly.express as px
import re
import os
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Output, Input
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.pool import NullPool
from dash import html
from dash import dcc



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

df = pd.read_csv('povertydata.csv')
df = df[['Country Name','year', 'Poverty gap at $5.50 a day (2011 PPP) (% of population)']]
df = df.dropna(subset=['Poverty gap at $5.50 a day (2011 PPP) (% of population)'])
df = df.sort_values(by='Poverty gap at $5.50 a day (2011 PPP) (% of population)')
df_years =sorted(set(df['year']))

cividis0 = px.colors.sequential.Cividis[0]

app.layout = html.Div([
     html.H1('Poverty and Equity Database'),
     html.Br(),
     dcc.Slider(id='pov_indicator',
         min=df_years[0],
         max=df_years[-1],
         step=1,
         dots=True,
         included=False,
         value=2018,
         marks={year: {
             'label': str(year),
             'style': {'color': cividis0}
         } for year in df_years[::5]}
     ),
     dcc.Graph(id='pov_scatter_chart')
])

@app.callback(Output('pov_scatter_chart', 'figure'), 
              Input('pov_indicator', 'value'))
def plot_poverty_scatter_plot(year, df=df):
    if not year:
         return ''      
    fig = px.scatter(
                  df,
                  x=df['Poverty gap at $5.50 a day (2011 PPP) (% of population)'],
                  y=df['Country Name'],
                  color='Country Name',
                  size=[30] * len(df),
                  size_max=15,
                  log_x=True, 
                  hover_name='Country Name',
                  height = 250 + (20 * len(df)),
                  color_continuous_scale='cividis',
                  color_continuous_midpoint=0,
                  title='Poverty Level'
    )          
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)