import dash
import dash_core_components as dcc
import dash_html_components as html

from app import Graphs

def generate_html(channel_name):

    layout = html.Div([

        html.H1(f'{channel_name} Creator Dashboard'),
        dcc.Link('return to home page', href='/'),

        # First pie graph with date range dropdown
        html.H2('Fan badge vs total comments'),
        html.H4('Date Range', style={'textAlign': 'left'}),
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
            style={'width': '500px'}
        ),
        html.Div(id='pie_graph'),

        # Interactive funnel Graph
        html.H2('Fan conversion rates'),
        html.Div([
            html.Label('Creator Responses'),
            dcc.Checklist(
                id='funnel_graph_checklist',
                options=[
                    {'label': 'First comment', 'value': 'first'},
                    {'label': 'Trending comment', 'value': 'trend'},
                ],
                value=[])
            ],
            style={'textAlign': 'center', 'width':'450px'}
        ),
        html.Div(
            html.Div(
                id='funnel_graph', 
                style={'width':'450px'}
            ),
            style={'display': 'flex', 'margin-right':'auto', 'margin-left': 'auto'}
        ),

        # Fan Conversion bars
        html.H2('Fan conversion bar graph'),
        html.Div(
            dcc.Graph(
                figure=Graphs.fan_conversion.bar_graph()
            ) 
        ),

        # Interactive sankey Graph
        html.H2('Fan conversion pipeline'),
        html.Div([
            html.Label('Creator Responses'),
            dcc.Checklist(
                id='sankey_graph_checklist',
                options=[
                    {'label': 'Hide Newfans with no response', 'value': 'first'},
                    {'label': 'Hide trendingFans with no response', 'value': 'trend'},
                ],
                value=[])
            ],
        ),
        html.Div(
            html.Div(
                id='sankey_graph', 
            ),
        ),
    ],

    style={'padding-left': "30vh", 'padding-right': "30vh"}
    )
    
    return layout