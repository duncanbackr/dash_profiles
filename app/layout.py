import dash
import dash_core_components as dcc
import dash_html_components as html

from app import Graphs

def generate_html(df_user, df_auth):

    layout = html.Div([

        html.H1('Creator Dashboard'),

        # First pie graph with date range dropdown
        html.H4('Date Range'),
        html.Div([
            dcc.Dropdown(
                id='pie_graph_dropdown',
                options=[
                    {'label': 'All Time', 'value': None},
                    {'label': 'Last two weeks', 'value': 14}, 
                    {'label': 'Last two months', 'value': 60},
                    {'label': 'Last twelve months', 'value': 365}],
                value=None),
            ],
            style={"width": "50%"},
        ),
        html.Div(id='pie_graph'),

        # Static funnel Graph
        dcc.Graph(figure=Graphs.funnel.get_funnel(df_user))

        ],

        style={'padding-left': "30vh", 'padding-right': "30vh"}
    )
    return layout