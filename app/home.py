import dash_core_components as dcc
import dash_html_components as html

from app import Backrest
from config import Config



def dropdown_layout():

    token = Backrest.authentication.get_token(Config.BACKREST_URL)
    users = Backrest.request.get_resource(resource='/v1/youtube/creators', params={}, token=token)
    
    layout = html.Div(
        [
            html.H1('Backr Creator Profiles'),
            html.H3('Select A Creator'),
            dcc.Dropdown(
                    id='home_dropdown',
                    options=[{'label': user['channel_name'], 'value': f"{user['channel_name']}/{user['channel_id']}"} for user in users],
                    value=None
                ),
            html.Div(id='dashboard_link'),
        ],
        style={'padding-left': "30vh", 'padding-right': "30vh"}
        )

    return layout