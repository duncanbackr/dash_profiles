import plotly.graph_objects as go

def get_metrics_table(df_user):
    df_top = df_user[df_user.active_label == 'topFan']
    num_top_fans = len(df_top['account_title'].unique())

    top_fan_list = list(df_top['account_title'].unique())

    num_comments_top_fans = len(df_user[df_user.account_title.isin(top_fan_list)])
    num_comments_total = len(df_user)

    df_trend = df_user[(df_user.active_label == 'trendingFan') & ~(df_user.account_title.isin(top_fan_list))]
    trend_fan_list = list(df_trend['account_title'].unique())
    num_trend_fans = len(df_trend['account_title'].unique())

    df_new = df_user[(df_user.active_label == 'newFan')& ~(df_user.account_title.isin(top_fan_list))& ~(df_user.account_title.isin(trend_fan_list))]
    new_fan_list = list(df_new['account_title'].unique())
    num_new_fans = len(df_new['account_title'].unique())

    df_re = df_user[(df_user.active_label == 'reEngageFan')& ~(df_user.account_title.isin(top_fan_list))& ~(df_user.account_title.isin(trend_fan_list)) & ~(df_user.account_title.isin(new_fan_list))]
    new_re_list = list(df_re['account_title'].unique())
    num_re_fans = len(df_re['account_title'].unique())

    df_top_pass = df_user[df_user.passive_label == 'TopFan']
    num_top_fans_pass = len(df_top_pass['account_title'].unique())
    top_fan_list_pass = list(df_top_pass['account_title'].unique())
    num_comments_top_fans_pass = len(df_user[df_user.account_title.isin(top_fan_list_pass)])

    df_trend_pass = df_user[(df_user.passive_label == 'TrendFan') & ~(df_user.account_title.isin(top_fan_list_pass))]
    trend_fan_list_pass = list(df_trend_pass['account_title'].unique())
    num_trend_fans_pass = len(df_trend_pass['account_title'].unique())

    df_new_pass = df_user[(df_user.passive_label == 'NewFan')& ~(df_user.account_title.isin(top_fan_list_pass))& ~(df_user.account_title.isin(trend_fan_list_pass))]
    new_fan_list_pass = list(df_new_pass['account_title'].unique())
    num_new_fans_pass = len(df_new_pass['account_title'].unique())

    top_fans_received_response_whenever = len(df_user[df_user.account_title.isin(top_fan_list_pass)][df_user.received_response]['account_title'].unique())
    top_fans_received_response_while_top_fan = len(df_top_pass[df_top_pass.received_response]['account_title'].unique())

    trend_fans_received_response_whenever = len(df_user[df_user.account_title.isin(trend_fan_list_pass)][df_user.received_response]['account_title'].unique())
    trend_fans_received_response_while_trend_fan = len(df_trend_pass[df_trend_pass.received_response]['account_title'].unique())

    new_fans_received_response = len(df_new[df_new_pass.received_response]['account_title'].unique())

    fig = go.Figure(data=[go.Table(header=dict(values=['Metric Name', 'Value']),
                    cells=dict(
                        values=[['Average number of comments by top fans', 'Proportion of comments by top fans' , 'Fan Type Ratio (New: Trend: Top: ReEngage)', 'Top Fan Response Rate', 
                                    'Trending Fan Response Rate', 'New Fan Response Rate'], 
                        [str(round(num_comments_top_fans/num_top_fans, 2)), str(round(num_comments_top_fans/num_comments_total, 4) * 100) + '%',  
                                    str(num_new_fans)+': '+str(num_trend_fans)+': '+str(num_top_fans) + ': '+str(num_re_fans), 
                                            str(round(top_fans_received_response_whenever/num_top_fans, 4) * 100) + '%', str(round(trend_fans_received_response_whenever/num_trend_fans, 4) * 100) + '%',
                                                    str(round(new_fans_received_response/num_new_fans, 4) * 100) + '%']]))
                        ])
    return fig