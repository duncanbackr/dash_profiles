import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_topfan_table(df_user):

    df_best_fans = df_user[['account_title', 'creator_responses', 'total_comments', 'active_label']]

    df_best_fans_top = df_best_fans[df_best_fans.active_label == 'topFan']
    df_best_fans_top_sort = df_best_fans_top.sort_values('total_comments', ascending=False)
    df_best_fans_top_sort_unique = df_best_fans_top_sort.drop_duplicates('account_title', keep ='first')[0:10]
    df_best_fans_top_sort_unique['response_rate'] = df_best_fans_top_sort_unique['creator_responses']/df_best_fans_top_sort_unique['total_comments']

    df_final = df_best_fans_top_sort_unique[['account_title','total_comments', 'response_rate' ]]

    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_final.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df_final.account_title, df_final.total_comments, df_final.response_rate],
            fill_color='lavender',
            align='left'))
    ])

    return fig