import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_trend_plot(df_user):

    df_timeline = df_user[["timestamp", "active_label", "fan_id"]]
    df_timeline_top = df_timeline[df_timeline.active_label == 'topFan']
    df_timeline_top = df_timeline_top.drop_duplicates("fan_id", keep = 'first')

    df_timeline_trend = df_timeline[df_timeline.active_label == 'trendingFan']
    df_timeline_trend = df_timeline_trend.drop_duplicates("fan_id", keep = 'first')

    df_timeline_new = df_timeline[df_timeline.active_label == 'newFan']
    df_timeline_new = df_timeline_new.drop_duplicates("fan_id", keep = 'first')

    df_timeline_re = df_timeline[df_timeline.active_label == 'reEngageFan']
    df_timeline_re = df_timeline_re.drop_duplicates("fan_id", keep = 'first')


    df_timeline_top['is_top_fan'] = True
    df_timeline_top['top_fan_cum_sum'] = df_timeline_top.is_top_fan.cumsum()

    df_timeline_trend['is_trend_fan'] = True
    df_timeline_trend['trend_fan_cum_sum'] = df_timeline_trend.is_trend_fan.cumsum()

    df_timeline_new['is_new_fan'] = True
    df_timeline_new['new_fan_cum_sum'] = df_timeline_new.is_new_fan.cumsum()

    df_timeline_re['is_re_fan'] = True
    df_timeline_re['re_fan_cum_sum'] = df_timeline_re.is_re_fan.cumsum()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df_timeline_top['timestamp'], y=df_timeline_top['top_fan_cum_sum'],
                      mode='lines+markers',
                      name='Top Fans'), secondary_y = True)
    fig.add_trace(go.Scatter(x=df_timeline_new['timestamp'], y=df_timeline_new['new_fan_cum_sum'],
                      mode='lines+markers',
                      name='New Fans'), secondary_y = False)
    fig.add_trace(go.Scatter(x=df_timeline_re['timestamp'], y=df_timeline_re['re_fan_cum_sum'] ,
                      mode='lines+markers',
                      name='ReEngaged Fans'), secondary_y = True)

  
    fig.update_layout(title='Fan Types over Time',
                  xaxis_title='Time',
                  yaxis_title='Total comments')
    return fig