import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import time

from app import Backrest, Process, Graphs, layout, home

def pull_data(pathname):
    path_elements = pathname.split('/')

    # Save data
    raw_data = Backrest.get_raw_data(path_elements[2])
    full_df = Process.get_full_df(raw_data)
    full_df.to_csv('full_df.csv', index=False)
    return path_elements[1]


def init_dashboard(server):

    dash_app = dash.Dash(server=server)

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    """ Set Dashboard Callbacks """

    @dash_app.callback(
        dash.dependencies.Output('dashboard_link', 'children'),
        dash.dependencies.Input('home_dropdown', 'value'))
    def display_value(path):
        return html.Div(dcc.Link(f'Creator page: {path}', href=path)) if path else None
    
    @dash_app.callback(
        dash.dependencies.Output('pie_graph', 'children'),
        dash.dependencies.Input('url', 'pathname'),
        dash.dependencies.Input('pie_graph_dropdown', 'value'),
    )
    def pie_callback(pathname, cutoff_days):
        if not os.path.exists('full_df.csv'):
            _ = pull_data(pathname)
        return dcc.Graph(
            figure= Graphs.pie_chart.active_label(cutoff_days)
        ) 

    @dash_app.callback(
        dash.dependencies.Output('funnel_graph', 'children'),
        dash.dependencies.Input('url', 'pathname'),
        dash.dependencies.Input('funnel_graph_checklist', 'value'))
    def funnel_callback(pathname, checkbox_data):
        if not os.path.exists('full_df.csv'):
            _ = pull_data(pathname)
        return dcc.Graph(
            figure=Graphs.funnel.get_funnel(checkbox_data)
        )

    @dash_app.callback(
        dash.dependencies.Output('response_table', 'children'),
        dash.dependencies.Input('url', 'pathname'),
        dash.dependencies.Input('response_table_dropdown', 'value'))
    def response_table_callback(pathname, badge):
        if not os.path.exists('full_df.csv'):
            _ = pull_data(pathname)
        return dcc.Graph(
            figure=Graphs.data_tables.creator_response_table(active_badge=badge)
        )

    @dash_app.callback(
        dash.dependencies.Output('sankey_graph', 'children'),
        dash.dependencies.Input('url', 'pathname'),
        dash.dependencies.Input('sankey_graph_checklist', 'value'))
    def sankey_callback(pathname, checkbox_data):
        if not os.path.exists('full_df.csv'):
            _ = pull_data(pathname)
        return dcc.Graph(
            figure=Graphs.sankey.get_sankey(checkbox_data)
        ) 

    """ Set the routing """

    @dash_app.callback(dash.dependencies.Output('page-content', 'children'),
                [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        if pathname != '/':
            
            channel_name = pull_data(pathname)
            time.sleep(0.5) # so that callbacks can find data

            return layout.generate_html(channel_name)
        else:
            return home.dropdown_layout()
    # You could also return a 404 "URL not found" page here
    
    return dash_app.server



