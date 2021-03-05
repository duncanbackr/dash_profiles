import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime,timedelta

def get_agg_metrics(df_user):

    one_week = datetime.today() - timedelta(days=7)
    two_week = datetime.today() - timedelta(days=14)
    two_week = two_week.date()
    one_week = one_week.date()

    current_week_df = df_user[df_user.timestamp >= pd.to_datetime(one_week)]
    last_week_df = df_user[(df_user.timestamp <= pd.to_datetime(one_week)) & (df_user.timestamp >= pd.to_datetime(two_week))]

    current_week_df_top = current_week_df[current_week_df['passive_label'] == 'TopFan']
    current_week_df_new = current_week_df[current_week_df['passive_label'] == 'NewFan']
    last_week_df_top = last_week_df[last_week_df['passive_label'] == 'TopFan']
    last_week_df_new = last_week_df[last_week_df['passive_label'] == 'NewFan']


    def get_metrics_last(current_week_df,last_week_df):
        comments_this_week_agg = sum(current_week_df.id.value_counts())
        comments_last_week_agg = sum(last_week_df.id.value_counts())

        if comments_last_week_agg != 0:
            comments_growth = round((comments_this_week_agg/comments_last_week_agg -1)*100, 1)
        else:
            comments_growth = 0

        replies_this_week_agg = len(current_week_df[current_week_df.received_response == 'True'])
        replies_last_week_agg = len(last_week_df[last_week_df.received_response == 'True'])

        if replies_last_week_agg != 0:
            replies_growth = round((replies_this_week_agg/replies_last_week_agg - 1)*100, 1)
        else:
            replies_growth = 0

        if comments_this_week_agg !=0:
            response_rate = round(replies_this_week_agg/comments_this_week_agg, 3)*100
        else:
            response_rate = 0
        A = [comments_this_week_agg, comments_last_week_agg, comments_growth, replies_this_week_agg, replies_last_week_agg, replies_growth, response_rate]
        df = pd.DataFrame([A])
        df.columns = ['commments_this_week', 'comments_last_week', 'comments_growth', 'responses_this_week', 'responses_last_week', 'responses_growth', 'response_rate']
        return df

    df1 = get_metrics_last(current_week_df,last_week_df)

    df_top = get_metrics_last(current_week_df_top,last_week_df_top)
    df_top.columns = df_top.columns + '_top'

    df_new = get_metrics_last(current_week_df_new,last_week_df_new)
    df_new.columns = df_new.columns + '_new'

    def active_fans_df(current_week_df, last_week_df):

        active_fans_this_week = len(current_week_df.account_title.unique())
        active_fans_last_week = len(last_week_df.account_title.unique())

        if active_fans_last_week != 0:
            active_fans_growth = round((active_fans_this_week/active_fans_last_week -1)*100, 1)
        else:
            active_fans_growth = 0

        A = [active_fans_this_week, active_fans_last_week, active_fans_growth]
        df = pd.DataFrame([A])
        df.columns = ['active_fans_this_week', 'active_fans_last_week', 'active_fans_growth']
        
        return df

    df2 = active_fans_df(current_week_df, last_week_df)
    df2_top = active_fans_df(current_week_df_top, last_week_df_top)
    df2_top.columns = df2_top.columns + '_top'
    df2_new = active_fans_df(current_week_df_new, last_week_df_new)
    df2_new.columns = df2_new.columns + '_new'

    df_concat = pd.concat([df1, df_top, df_new, df2, df2_top, df2_new], axis=1)

    
    fig = go.Figure(data=[go.Table(header=dict(values=['Metric Name', 'Value']),
                 cells=dict(values=[df_concat.columns, df_concat.iloc[0]]))
                     ])

    return fig