import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = go.Figure()

app.layout = html.Div([
    html.H1('Yooh, Hello there?'),
    #fig.add_scatter(x=[1,2,3], y=[4,5,6])

])

fig.add_scatter(x=[1,2,3], y=[4,5,6])
fig.show()

if __name__ == "__main__":
    app.run_server(debug=True)