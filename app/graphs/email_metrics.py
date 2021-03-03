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

    comments_this_week_agg = current_week_df.groupby(['channel_name'])['video_title'].count().reset_index(name = 'count')
    comments_last_week_agg = last_week_df.groupby(['channel_name'])['video_title'].count().reset_index(name ='count')

    comments_agg = pd.merge(comments_this_week_agg, comments_last_week_agg, on = ['channel_name'], how = 'outer')

    comments_agg['count_x'] = comments_agg['count_x'].fillna(0)
    comments_agg['growth'] = 100*(round(comments_agg['count_x']/comments_agg['count_y'],2)-1)
    comments_agg['count_y'] = comments_agg['count_y'].fillna(0)
    comments_agg['growth'] = comments_agg['growth'].fillna(100)                          
    comments_agg.columns = ['channel_name', 'commments_this_week', 'comments_last_week', 'comments_growth']
    replies_this_week_agg = current_week_df.groupby(['channel_name'])['parent_comment_id'].nunique().reset_index(name = 'count')
    replies_last_week_agg = last_week_df.groupby(['channel_name'])['parent_comment_id'].nunique().reset_index(name ='count')

    responses_agg = pd.merge(replies_this_week_agg, replies_last_week_agg, on = ['channel_name'], how = 'outer')

    responses_agg['count_x'] = responses_agg['count_x'].fillna(0)
    responses_agg['growth'] = 100*(round(responses_agg['count_x']/responses_agg['count_y'],2)-1)
    responses_agg['count_y'] = responses_agg['count_y'].fillna(0)
    responses_agg['growth'] = responses_agg['growth'].fillna(100)                           
    responses_agg.columns = ['channel_name', 'responses_this_week', 'responses_last_week', 'responses_growth' ]

    df1_agg = pd.merge(comments_agg, responses_agg, on = ['channel_name'], how = 'outer')
    df1_agg['response_rate'] = round(df1_agg['responses_this_week']/df1_agg['commments_this_week'], 3)*100
    df1_agg['response_rate'] = df1_agg['response_rate'].fillna(0) 
    df1_agg = df1_agg.fillna(0)

    current_week_df_top = current_week_df[current_week_df['passive_label'] == 'TopFan']
    current_week_df_new = current_week_df[current_week_df['passive_label'] == 'NewFan']
    last_week_df_top = last_week_df[last_week_df['passive_label'] == 'TopFan']
    last_week_df_new = last_week_df[last_week_df['passive_label'] == 'NewFan']

    comments_this_week_top_agg = current_week_df_top.groupby(['channel_name'])['video_title'].count().reset_index(name = 'count')
    comments_last_week_top_agg = last_week_df_top.groupby(['channel_name'])['video_title'].count().reset_index(name ='count')

    comments_top_agg = pd.merge(comments_this_week_top_agg, comments_last_week_top_agg, on = ['channel_name'], how = 'outer')

    comments_top_agg['count_x'] = comments_top_agg['count_x'].fillna(0)
    comments_top_agg['growth'] = 100*(round(comments_top_agg['count_x']/comments_top_agg['count_y'],2)-1)
    comments_top_agg['count_y'] = comments_top_agg['count_y'].fillna(0)
    comments_top_agg['growth'] = comments_top_agg['growth'].fillna(100)  


    replies_this_week_top_agg = current_week_df_top.groupby(['channel_name'])['parent_comment_id'].nunique().reset_index(name = 'count')
    replies_last_week_top_agg = last_week_df_top.groupby(['channel_name'])['parent_comment_id'].nunique().reset_index(name ='count')

    responses_top_agg = pd.merge(replies_this_week_top_agg, replies_last_week_top_agg, on = ['channel_name'], how = 'outer')
    responses_top_agg['count_x'] = responses_top_agg['count_x'].fillna(0)
    responses_top_agg['count_x'] = responses_top_agg['count_x'].fillna(0)
    responses_top_agg['growth'] = 100*(round(responses_top_agg['count_x']/responses_top_agg['count_y'],2)-1)
    responses_top_agg['response_rate'] = round(responses_top_agg['count_x']/comments_top_agg['count_x'],3)*100

    responses_top_agg['count_y'] = responses_top_agg['count_y'].fillna(0)
    responses_top_agg['growth'] = responses_top_agg['growth'].fillna(100)                          
    responses_top_agg['response_rate'] = responses_top_agg['response_rate'].fillna(0) 

    top_fans_agg = pd.merge(comments_top_agg, responses_top_agg, on = ['channel_name'], how = 'outer')
    top_fans_agg.columns = ['comments_this_week_top', 'channel_name', 'comments_last_week_top', 'change_comments_top_growth', 'responses_this_week_top','responses_last_week_top','change_responses_top_growth', 'response_rate_top']
    top_fans_agg['response_rate_top'] = top_fans_agg['response_rate_top'].fillna(0) 

    comments_this_week_new_agg = current_week_df_new.groupby(['channel_name'])['video_title'].count().reset_index(name = 'count')
    comments_last_week_new_agg = last_week_df_new.groupby(['channel_name'])['video_title'].count().reset_index(name ='count')

    comments_new_agg = pd.merge(comments_this_week_new_agg, comments_last_week_new_agg, on = ['channel_name'], how = 'outer')

    comments_new_agg['count_x'] = comments_new_agg['count_x'].fillna(0)
    comments_new_agg['growth'] = 100*(round(comments_new_agg['count_x']/comments_new_agg['count_y'],2)-1)
    comments_new_agg['count_y'] = comments_new_agg['count_y'].fillna(0)
    comments_new_agg['growth'] = comments_new_agg['growth'].fillna(100)  


    replies_this_week_new_agg = current_week_df_new.groupby(['channel_name'])['parent_comment_id'].nunique().reset_index(name = 'count')
    replies_last_week_new_agg = last_week_df_new.groupby(['channel_name'])['parent_comment_id'].nunique().reset_index(name ='count')

    responses_new_agg = pd.merge(replies_this_week_new_agg, replies_last_week_new_agg, on = ['channel_name'], how = 'outer')

    responses_new_agg['count_x'] = responses_new_agg['count_x'].fillna(0)
    responses_new_agg['growth'] = 100*(round(responses_new_agg['count_x']/responses_new_agg['count_y'],2)-1)
    responses_new_agg['response_rate'] = round(responses_top_agg['count_x']/comments_new_agg['count_x'],3)*100

    responses_new_agg['count_y'] = responses_new_agg['count_y'].fillna(0)
    responses_new_agg['growth'] = responses_new_agg['growth'].fillna(100)                          

    new_fans_agg = pd.merge(comments_new_agg, responses_new_agg, on = ['channel_name'], how = 'outer')
    new_fans_agg.columns = ['channel_name', 'comments_this_week_new', 'comments_last_week_new', 'change_comments_new_growth', 'responses_this_week_new','responses_last_week_new','change_responses_new_growth', 'response_rate_new' ]

    df2_agg = pd.merge(top_fans_agg, new_fans_agg, on =['channel_name'])
    df2_agg = df2_agg.fillna(0)

    active_fans_current_week = current_week_df.groupby(['account_title', 'channel_name'])['account_title'].unique().reset_index(name = 'fan')
    active_fans_current_week = active_fans_current_week.groupby(['channel_name'])['channel_name'].count().reset_index(name = 'count')

    active_fans_last_week = last_week_df.groupby(['account_title', 'channel_name'])['account_title'].unique().reset_index(name = 'fan')
    active_fans_last_week = active_fans_last_week.groupby(['channel_name'])['channel_name'].count().reset_index(name = 'count')

    active_fans = pd.merge(active_fans_current_week, active_fans_last_week, on = 'channel_name', how = 'outer')
    active_fans['count_x'] = active_fans['count_x'].fillna(0)
    active_fans['growth'] =  round((active_fans['count_x']/active_fans['count_y'] - 1)*100, 3)
    active_fans['growth'] = active_fans['growth'].fillna(100)
    active_fans['count_y'] = active_fans['count_y'].fillna(100)
    active_fans.columns = ['channel_name', 'active_fans_this_week', 'active_fans_last_week', 'active_fans_growth']

    df3_agg = pd.merge(df1_agg, df2_agg, on = 'channel_name', how= 'outer')
    df3_agg = df3_agg.fillna(0)

    df_final_agg = pd.merge(df3_agg, active_fans, on = 'channel_name', how = 'outer')
    df_final_agg = df_final_agg.fillna(0)

    fig = go.Figure(data=[go.Table(header=dict(values=['Metric Name', 'Value']),
                    cells=dict(values=[df_final_agg.columns, df_final_agg.iloc[0]]))
                        ])
    return fig.show()