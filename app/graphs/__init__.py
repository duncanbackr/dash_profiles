from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#from Graphs.df_active_fan_trend import activeFans_fig
from Graphs.bubble import bubble_fig
#from Graphs.df_day import  fig_day
#from Graphs.df_time import df_time_auth, df_time_user, fig_time
#from main.graphs.df_topfan import df_topfan, fig_topfan
# from Graphs.df_video_timeline import fig_video_timeline
# from Graphs.df_first_month_comparison import fig_video_comparison
# from Graphs.df_fan_table import get_table, fig_table
# from Graphs.funnel import fig_funnel_to_bar
from Graphs.funnel import get_funnel
from Graphs.pie_chart import get_active_label_pie


def get_layout(df):

    fig_pie = get_active_label_pie(df)
    fig_funnel = get_funnel(df)
    fig_bubble = bubble_fig(df)

    layout = html.Div(children=[
        html.H1(children='Creator Dashboards'),
        html.Div(children='''Analytics to help Creators grow their engagements'''),
            dcc.Graph(id='example-graph',figure=fig_pie),
            dcc.Graph(id='example-graph',figure=fig_funnel),
            dcc.Graph(id='example-graph',figure=fig_bubble)

        ]
    )
    return layout