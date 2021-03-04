import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_funnel(df_fans):

    df_fans['newfan_response'] = (df_fans.passive_label == 'NewFan') & (df_fans.received_response == True)
    df_fans['trend_fan'] = (df_fans.passive_label == 'TrendFan')
    df_fans['trend_response'] = (df_fans.passive_label == 'TrendFan') & (df_fans.received_response == True)
    df_fans['top_fan'] = (df_fans.passive_label == 'TopFan')

    ### group by fan and agregate each column ###
    fan_funnel = df_fans.groupby('account_title').agg(
            {
                'newfan_response':'sum',
                'trend_fan':'sum',
                'trend_response':'sum',
                'top_fan':'sum'
            }
        ).astype(bool)

    no_first_new = sum(~fan_funnel['newfan_response'])
    yes_first_new = sum(fan_funnel['newfan_response'])
    no_first_trend = sum(~fan_funnel['newfan_response'] & fan_funnel['trend_fan'])
    yes_first_trend = sum(fan_funnel['newfan_response'] & fan_funnel['trend_fan'])
    no_first_no_trend_top   = sum(~fan_funnel['newfan_response'] & ~fan_funnel['trend_response'] & fan_funnel['top_fan'])
    no_first_yes_trend_top  = sum(~fan_funnel['newfan_response'] &  fan_funnel['trend_response'] & fan_funnel['top_fan'])
    yes_first_no_trend_top  = sum( fan_funnel['newfan_response'] & ~fan_funnel['trend_response'] & fan_funnel['top_fan'])
    yes_first_yes_trend_top = sum( fan_funnel['newfan_response'] &  fan_funnel['trend_response'] & fan_funnel['top_fan'])

    y = ['New Fans', 'Trending Fans', 'Top Fans']
    fig = make_subplots(rows=1, cols=4)
    fig.add_trace(
        go.Funnel(
            name = 'First comment response and trending fan response',
            orientation = "h",
            y = y,
            x = [yes_first_new, yes_first_trend, yes_first_yes_trend_top],
            #x = [1, trend_with_first_response/first_with_response, topfan_yes_first_yes_trend_response/first_with_response],
            textinfo = "value+percent initial"
            ),
            row=1,col=1
        )
    fig.add_trace(
        go.Funnel(
            name = 'First comment response no trend fan response',
            orientation = "h",
            y = [' ','  ','   '], #y,
            x = [yes_first_new, yes_first_trend, yes_first_no_trend_top],
            #x = [1, trend_with_first_response/first_with_response, topfan_yes_first_no_trend_response/first_with_response],
            textinfo = "value+percent initial"
            ),
            row=1,col=2
        )
    fig.add_trace(
        go.Funnel(
            name = 'No first response yes trend fan response',
            orientation = "h",
            y = [' ','  ','   '], #y,
            x = [no_first_new, no_first_trend, no_first_yes_trend_top],
            #x = [1, trend_no_first_response/first_no_response, topfan_no_first_yes_trend_response/first_no_response],
            textinfo = "value+percent initial"
            ),
            row=1,col=3
        )
    fig.add_trace(
        go.Funnel(
            name = 'No first response no trend fan response',
            orientation = "h",
            y = [' ','  ','   '], #y,
            x = [no_first_new, no_first_trend, no_first_no_trend_top],
            #x = [1, trend_no_first_response/first_no_response, topfan_no_first_no_trend_response/first_no_response],
            textinfo = "value+percent initial"
            ),
            row=1,col=4
        )
    return fig