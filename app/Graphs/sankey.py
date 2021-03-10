import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_sankey(callback_data):

    full_df = pd.read_csv('full_df.csv')
    df_user = full_df[full_df.by_creator == False]

    df_user['newfan_response'] = (df_user.static_badge == 'newFan') & (df_user.received_response == True)
    df_user['trend_fan'] = (df_user.static_badge == 'trendingFan')
    df_user['trend_response'] = (df_user.static_badge == 'trendingFan') & (df_user.received_response == True)
    df_user['top_fan'] = (df_user.static_badge == 'topFan')

    ### group by fan and agregate each column ###
    fan_funnel = df_user.groupby('fan_id').agg(
            {
                'newfan_response':'sum',
                'trend_fan':'sum',
                'trend_response':'sum',
                'top_fan':'sum'
            }
        ).astype(bool)

    # Create funnel groupings
    no_first = sum(~fan_funnel['newfan_response'])
    yes_first = sum(fan_funnel['newfan_response'])
    no_first_trend = sum(~fan_funnel['newfan_response'] & fan_funnel['trend_fan'])
    yes_first_trend = sum(fan_funnel['newfan_response'] & fan_funnel['trend_fan'])
    no_first_churn = sum(~fan_funnel['newfan_response'] & ~fan_funnel['trend_fan'])
    yes_first_churn = sum(fan_funnel['newfan_response'] & ~fan_funnel['trend_fan'])
    trend = sum(fan_funnel['trend_fan'])
    yes_trend = sum(fan_funnel['trend_response'])
    no_trend = trend - yes_trend
    yes_trend_top = sum(fan_funnel['trend_fan'] & fan_funnel['trend_response'] & fan_funnel['top_fan'])
    no_trend_top = sum(fan_funnel['trend_fan'] & ~fan_funnel['trend_response'] & fan_funnel['top_fan'])
    yes_trend_churn = sum(fan_funnel['trend_fan'] & fan_funnel['trend_response'] & ~fan_funnel['top_fan'])
    no_trend_churn = sum(fan_funnel['trend_fan'] & ~fan_funnel['trend_response'] & ~fan_funnel['top_fan'])

    no_first_no_trend_top   = sum(~fan_funnel['newfan_response'] & ~fan_funnel['trend_response'] & fan_funnel['top_fan'])
    no_first_yes_trend_top  = sum(~fan_funnel['newfan_response'] &  fan_funnel['trend_response'] & fan_funnel['top_fan'])
    yes_first_no_trend_top  = sum( fan_funnel['newfan_response'] & ~fan_funnel['trend_response'] & fan_funnel['top_fan'])
    yes_first_yes_trend_top = sum( fan_funnel['newfan_response'] &  fan_funnel['trend_response'] & fan_funnel['top_fan'])

    full_link = dict(
    source = [0, 1, 0, 1, 2, 2, 4, 5, 4, 5], 
    target = [2, 2, 3, 3, 4, 5, 6, 6, 7, 7],
    value = [yes_first_trend, no_first_trend, yes_first_churn, no_first_churn,
                yes_trend, no_trend,
                yes_trend_top, no_trend_top, yes_trend_churn, no_trend_churn]
                )

    hide_new = dict(
    source = [0, 0, 2, 2, 4, 5, 4, 5], 
    target = [2, 3, 4, 5, 6, 6, 7, 7],
    value = [yes_first_trend, yes_first_churn, 
            yes_trend, no_trend,
                yes_trend_top, no_trend_top, yes_trend_churn, no_trend_churn]
                )

    hide_trend = dict(
    source = [0, 1, 0, 1, 2, 4, 4], 
    target = [2, 2, 3, 3, 4, 6, 7],
    value = [yes_first_trend, no_first_trend, yes_first_churn, no_first_churn,
                yes_trend, 
                yes_trend_top, yes_trend_churn]
                )

    hide_new_hide_trend = dict(
    source = [0, 0, 2, 4, 4], 
    target = [2, 3, 4, 6, 7],
    value = [yes_first_trend, yes_first_churn,
                yes_trend,
                yes_trend_top, yes_trend_churn]
                )

    # Apply logic based on callbacks
    if 'first' in callback_data:
        link_data = hide_new

        if 'trend' in callback_data:
            link_data = hide_new_hide_trend

    else:
        link_data = full_link

        if 'trend' in callback_data:
            link_data = hide_trend


    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ["New Fans with response", "New Fans no response", "Trending", "Churned", "Trending with Response", "Trending no Response", "Top Fan", "churned"],
        color = "blue"
        ),
        link = link_data
        )])

    fig.update_layout(title_text="Fan flow Diagram, (static labels)", font_size=10)

    return fig