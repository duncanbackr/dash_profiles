import dash
import dash_core_components as dcc
import time

from app import Backrest, Process, Graphs, layout


def init_dashboard(server):

    dash_app = dash.Dash(server=server)

    # raw_data = Backrest.get_raw_data('UCGtHgazkYWXCecFs-OtJc1A')
    # df = Process.get_full_df(raw_data)
    import pandas as pd
    import os
    df = pd.read_csv(os.getcwd() + '/marspeed_full_data.csv')

    df_user = Process.get_df_user(df)
    df_auth = Process.get_auth_df(df)

    dash_app.layout = layout.generate_html(df_user, df_auth)
    
    @dash_app.callback(
        dash.dependencies.Output('pie_graph', 'children'),
        dash.dependencies.Input('pie_graph_dropdown', 'value'))
    def pie_callback(cutoff_days):
        return dcc.Graph(figure= Graphs.pie_chart.active_label(df_user, cutoff_days)) 
    
    return dash_app.server



