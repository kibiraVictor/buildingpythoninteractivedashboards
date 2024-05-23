import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Poverty And Equity Database', style={
        'color': 'blue',
        'fontsize': '40px'
    }),
    html.H2('The World Bank'),
    html.Br(),
    #html.P('Key Facts'),
    dcc.Dropdown(id='color_dropdown', options=[{
        'label': color, 'value': color
    } for color in ['blue','green','yellow']]),
    html.Div(id='color_output'),
    html.Br(),
    dbc.Tabs([
        dcc.Tab([
            html.Ul([
            html.Li('Number of Economies: 170'),
            html.Li('Temporal Coverage: 1974-2019'),
            html.Li('Update Frequencies: Quarterly'),
            html.Li('Last Updated: March 18, 2020'),
            html.Li([
            'Source: ',
            html.A('https://datacatalog.org/dataset/poverty-and-equity-database', href='https://datacatalog-worldbank.org/dataset/poverty-and-equity-database')
        ])
    ])

        ], label='Key Facts'),
    dbc.Tab([
        html.Ul([
            html.Br(),
            html.Li('Book Title: Interactive Dashboards and Data Apps'),
            html.Li(['Github repo: ',
                    html.A(
                        'https://github.com/PackitPublishing/InteractiveDashboards',   href='https://github.com/PackitPublishing'
                    )
                    ])
        ])
    ], label='Project Info')
    ])
    
])

#standalone python function and the callback funtion
#output has to be provided before the inputs
@app.callback(Output('color_output', 'children'),
              Input('color_dropdown', 'value'))
def display_color_selected(color):
    if color is None:
        color='Nothing'
    return 'You selected ' + color

if __name__ == "__main__":
    app.run_server(debug=True, port=8060)