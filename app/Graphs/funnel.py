import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_funnel(callback_data):

    full_df = pd.read_csv(os.getcwd() + '/full_df.csv')
    df_user = full_df[full_df.by_creator == False]

    df_user['newfan_response'] = (df_user.passive_label == 'NewFan') & (df_user.received_response == True)
    df_user['trend_fan'] = (df_user.passive_label == 'TrendFan')
    df_user['trend_response'] = (df_user.passive_label == 'TrendFan') & (df_user.received_response == True)
    df_user['top_fan'] = (df_user.passive_label == 'TopFan')

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
    no_first_new = sum(~fan_funnel['newfan_response'])
    yes_first_new = sum(fan_funnel['newfan_response'])
    no_first_trend = sum(~fan_funnel['newfan_response'] & fan_funnel['trend_fan'])
    yes_first_trend = sum(fan_funnel['newfan_response'] & fan_funnel['trend_fan'])
    no_first_no_trend_top   = sum(~fan_funnel['newfan_response'] & ~fan_funnel['trend_response'] & fan_funnel['top_fan'])
    no_first_yes_trend_top  = sum(~fan_funnel['newfan_response'] &  fan_funnel['trend_response'] & fan_funnel['top_fan'])
    yes_first_no_trend_top  = sum( fan_funnel['newfan_response'] & ~fan_funnel['trend_response'] & fan_funnel['top_fan'])
    yes_first_yes_trend_top = sum( fan_funnel['newfan_response'] &  fan_funnel['trend_response'] & fan_funnel['top_fan'])

    # Apply logic based on callbacks
    if 'first' in callback_data:
      row_1_data = yes_first_new
      row_2_data = yes_first_trend

      if 'trend' in callback_data:
        row_3_data = yes_first_yes_trend_top
      else:
        row_3_data = yes_first_no_trend_top

    else:
      row_1_data = no_first_new
      row_2_data = no_first_trend

      if 'trend' in callback_data:
        row_3_data = no_first_yes_trend_top
      else:
        row_3_data = no_first_no_trend_top

    y = ['New Fans', 'Trending Fans', 'Top Fans']
    fig = go.Figure(go.Funnel(
            name = 'First comment response and trending fan response',
            orientation = "h",
            y = y,
            x = [row_1_data, row_2_data, row_3_data],
            textinfo = "value+percent initial"
            )
    )
    return fig