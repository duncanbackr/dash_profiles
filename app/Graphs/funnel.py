import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_funnel(df_fans, callback_data):

    df_fans['newfan_response'] = (df_fans.passive_label == 'NewFan') & (df_fans.received_response == True)
    df_fans['trend_fan'] = (df_fans.passive_label == 'TrendFan')
    df_fans['trend_response'] = (df_fans.passive_label == 'TrendFan') & (df_fans.received_response == True)
    df_fans['top_fan'] = (df_fans.passive_label == 'TopFan')

    ### group by fan and agregate each column ###
    fan_funnel = df_fans.groupby('fan_id').agg(
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