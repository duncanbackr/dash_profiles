import json 
import pandas as pd
from datetime import datetime,timedelta
import Process
import Graphs
import Backrest

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

raw_data = Backrest.get_raw_data('UCGtHgazkYWXCecFs-OtJc1A')

df = Process.get_full_df(raw_data)
df_user = Process.get_df_user(df)
df_auth = Process.get_auth_df(df)

app.layout = Graphs.get_layout(df_user, df_auth)

if __name__ == '__main__':
    app.run_server(debug=False)