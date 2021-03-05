import dash
import dash_core_components as dcc
import dash_html_components as html

from app import Graphs

def generate_html(df_user, df_auth):

    # fig_pie = get_active_label_pie(df_user)
    # fig_funnel = get_funnel(df_user)
    # fig_bubble = bubble_fig(df_user)
    # fig_time_of_day = fig_time(df_user, df_auth)

    layout = html.Div([

        html.H1('Creator Dashboard'),

        # First pie graph with dropdown
        dcc.Dropdown(
            id='pie_graph_dropdown',
            options=[
                {'label': 'Fans', 'value': 'fans'},
                {'label': 'Comments', 'value': 'comments'}, 
                {'label': 'Both', 'value': 'both'}],
            value='Fans'),
        html.Div(id='pie_graph'),

        # Static funnel Graph
        dcc.Graph(figure=Graphs.funnel.get_funnel(df_user))

        ],

        style={'padding-left': "30vh", 'padding-right': "30vh"}
    )
    return layout