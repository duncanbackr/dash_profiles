import pandas as pd
import plotly.graph_objects as go

def quotiant(numinator, denominator):
    if denominator == 0:
        return 0
    return numinator / denominator

def bar_graph():

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

    # First bar groupings
    all_first_trend = quotiant(sum(fan_funnel['trend_fan']), len(fan_funnel))
    no_first_trend = quotiant(sum(~fan_funnel['newfan_response'] & fan_funnel['trend_fan']), sum(~fan_funnel['newfan_response']))
    yes_first_trend = quotiant(sum(fan_funnel['newfan_response'] & fan_funnel['trend_fan']), sum(fan_funnel['newfan_response']))

    # Seccond bar groupings
    all_trend_top = quotiant(sum(fan_funnel['top_fan']), sum(fan_funnel['trend_fan']))
    no_trend_top = quotiant(sum(~fan_funnel['trend_response'] & fan_funnel['top_fan']), sum(~fan_funnel['trend_response']))
    yes_trend_top = quotiant(sum(fan_funnel['trend_response'] & fan_funnel['top_fan']), sum(fan_funnel['trend_response']))

    # Rounding values
    no_response_y = [round(x*100, 1) for x in [no_first_trend, no_trend_top]]
    all_response_y = [round(x*100, 1) for x in [all_first_trend, all_trend_top]]
    yes_response_y = [round(x*100, 1) for x in [yes_first_trend, yes_trend_top]]

    labels=['New Fan - Trend Fan', 'Trend Fan - Top Fan']

    fig = go.Figure(data=[
        go.Bar(
            name='Without Response', 
            x=labels, 
            y=no_response_y, 
            text = no_response_y, 
            textposition='auto'),
        go.Bar(
            name='Average', 
            x=labels, 
            y=all_response_y, 
            text = all_response_y, 
            textposition='auto'),
        go.Bar(
            name='With Response', 
            x=labels, 
            y=yes_response_y, 
            text = yes_response_y, 
            textposition='auto')
        ]
    )
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_xaxes(showgrid=False, zeroline=True)
    fig.update_yaxes(showgrid=False, zeroline=True)

    fig.update_layout(title='Fan Conversion Rates With/Without Response (Static badge)',
                    xaxis_title='Fan Conversion Type',
                    yaxis_title='Percent of Fans')

    return fig