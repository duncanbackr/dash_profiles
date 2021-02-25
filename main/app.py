import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from main.dropdown_layout import dropdown_layout
# from main.dashboard import dashboard_layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = dropdown_layout()

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return {'success': True}

if __name__ == '__main__':
    app.run_server(debug=False)