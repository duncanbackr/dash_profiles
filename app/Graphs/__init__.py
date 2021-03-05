from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Graphs.time_line import fig_time
from Graphs.funnel import get_funnel
from Graphs.pie_chart import get_active_label_pie
from Graphs.email_metrics import get_agg_metrics
from Graphs.trend import get_trend_plot
from Graphs.conversion_bar import fig_funnel_to_bar
from Graphs.top_fan_table import get_topfan_table
from Graphs.response_rate_table import get_metrics_table
from Graphs.video_bar import get_video_plot
from Graphs.day_bar import fig_day
from Graphs.df_video_timeline import fig_video_timeline
from Graphs.df_first_month_comparison import fig_video_comparison
from Graphs.df_active_fan_trend import activeFans_fig
from Graphs.bubble import bubble_fig

def get_layout(df_user, df_auth):

    fig_pie = get_active_label_pie(df_user)
    fig_funnel = get_funnel(df_user)
    fig_metrics = get_agg_metrics(df_user)
    fig_trend = get_trend_plot(df_user)
    fig_conversion = fig_funnel_to_bar(df_user)
    fig_topfans = get_topfan_table(df_user)
    fig_metrics2 = get_metrics_table(df_user)
    fig_vidbar = get_video_plot(df_user)
    fig_daybar = fig_day(df_user, df_auth)
    fig_timeline1 = fig_video_timeline(df_user)
    #fig_timeline2 = fig_video_comparison(df_user)
    fig_activefans = activeFans_fig(df_user)
    #fig_bubble = bubble_fig(df_user)
    #fig_time_of_day = fig_time(df_user, df_auth)

    layout = html.Div(children=[
        html.H1(children='Creator Dashboards'),
        html.Div(children='''Analytics to help Creators grow their engagements'''),
            dcc.Graph(id='example-graph',figure=fig_pie),
            dcc.Graph(id='example-graph2',figure=fig_funnel),
            dcc.Graph(id='example-graph3',figure=fig_metrics),
            dcc.Graph(id='example-graph4',figure=fig_trend),
            dcc.Graph(id='example-graph5',figure=fig_conversion),
            dcc.Graph(id='example-graph6',figure=fig_topfans),
            dcc.Graph(id='example-graph7',figure=fig_metrics2),
            dcc.Graph(id='example-graph8',figure=fig_vidbar),
            dcc.Graph(id='example-graph9',figure=fig_daybar),
            dcc.Graph(id='example-graph10',figure=fig_timeline1),
            #dcc.Graph(id='example-graph11',figure=fig_timeline2)
            dcc.Graph(id='example-graph12',figure=fig_activefans)
            #dcc.Graph(id='example-graph13',figure=fig_time_of_day)
            #dcc.Graph(id='example-graph14',figure=fig_bubble)

        ]
    )
    return layout