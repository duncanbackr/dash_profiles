import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def find_converation_fraction(df_cumcount, fan_list, lower_bound, upper_bound):
    if len(fan_list) == 0:
        return 0

    df_cumcount = df_cumcount.set_index('account_title')
    fans = df_cumcount.loc[fan_list]
    reponse_fraction = sum(fans.cum_count == upper_bound) / sum(fans.cum_count == lower_bound)
    return reponse_fraction

def fig_funnel_to_bar(df_fans):

    # Find new fans with first reponse
    new_fans_with_response = (df_fans[(df_fans.cum_count == 1) & (df_fans.received_response == True)]
                                .account_title
                                .to_list()
                             )
    
    # Find new fans without first reponse
    new_fans_no_response = (df_fans[(df_fans.cum_count == 1) & (df_fans.received_response == False)]
                                .account_title
                                .to_list()
                           )

    # Find funnel Values
    with_response_length = len(new_fans_with_response)
    with_response_fraction = find_converation_fraction(df_fans, new_fans_with_response, upper_bound =2, lower_bound=1)
    no_response_length = len(new_fans_no_response)
    no_response_fraction = find_converation_fraction(df_fans, new_fans_no_response,  upper_bound =2, lower_bound=1)

    trend_fans_with_response = (df_fans[(df_fans.passive_label == 'TrendFan') & (df_fans.received_response == True)]
                                .account_title
                                .unique()
                                .tolist()
                                )
    
    # Find all trend fans, and remove fans with response
    trend_fans_no_response = (df_fans[df_fans.passive_label == 'TrendFan']                            
                            .account_title
                            .unique()
                            .tolist()
                            )
    for x in trend_fans_with_response:
        trend_fans_no_response.remove(x)



    top_fan_cutoff = df_fans[df_fans.passive_label == 'TopFan'].cum_count.min()

    # Find funnel Values
    with_response_length_top = len(trend_fans_with_response)

    with_response_fraction_top = find_converation_fraction(df_fans, 
                                                    trend_fans_with_response,
                                                    upper_bound=top_fan_cutoff, 
                                                    lower_bound=2)
    no_response_length_top = len(trend_fans_no_response)
    no_response_fraction_top = find_converation_fraction(df_fans, 
                                                    trend_fans_no_response,  
                                                    upper_bound=top_fan_cutoff, 
                                                    lower_bound=2)

    text_response = [with_response_length, with_response_length_top]
    text_no_response = [no_response_length, no_response_length_top]

    labels=['New Fan - Trend Fan', 'Trend Fan - Top Fan']
    with_response_y = [with_response_fraction*100, with_response_fraction_top*100]
    rounded_with_response_y = [round(x, 1) for x in with_response_y]

    no_response_y = [no_response_fraction*100, no_response_fraction_top*100]
    rounded_no_response_y = [round(x, 1) for x in no_response_y]

    fig = go.Figure(data=[
        go.Bar(
            name='With Response', 
            x=labels, 
            y=with_response_y, 
            text = rounded_with_response_y, 
            textposition='outside'),
        go.Bar(
            name='Without Response', 
            x=labels, 
            y=no_response_y, 
            text = rounded_no_response_y, 
            textposition='outside')
                        ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_xaxes(showgrid=False, zeroline=True)
    fig.update_yaxes(showgrid=False, zeroline=True)

    fig.update_layout(title='Fan Conversion Rates With/Without Response',
                    xaxis_title='Fan Conversion Type',
                    yaxis_title='Percent of Fans')
    return fig