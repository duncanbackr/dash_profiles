import dash_core_components as dcc
import dash_html_components as html

def dropdown_layout():
    users = ['test', 'I am here']
    
    layout = html.Div(
        [
            html.H2('Select A Creator'),
            dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in users],
                    value=''
                ),
            html.Div(id='display-value'),
        ],
        style={'padding-left': "15vh", 'padding-right': "15vh"}
        )

    return layout