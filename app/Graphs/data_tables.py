
import pandas as pd
from datetime import timedelta
import plotly.graph_objects as go

def creator_response_table(active_badge=None):

    full_df = pd.read_csv('full_df.csv')
    full_df.timestamp = pd.to_datetime(full_df.timestamp)
    
    if active_badge:
        df_user = full_df[(full_df.by_creator == False) & (full_df.active_badge == active_badge)]
    
    else:
        df_user = full_df[full_df.by_creator == False]
    
    # Total comments - by date range # growth percentage
    # Total responses - by date range # growth percentage
    # Total unique fans - by date range # growth percentage

    stats_table = pd.DataFrame(
        index=['Total comments', 'Total responses', 'Response percentage %', 'Total unique fans'],
        columns=['Last 7 days', '7 - 14 days', 'Last 14 days', '14 - 28 days', 'Last 30 days', '30 - 60 days'])

    now = pd.Timestamp.utcnow()
    for (end_delay, start_delay), col_name in zip([(0, 7), (7, 14), (0, 14), (14, 28), (0, 30), (30, 60)], stats_table.columns):
        end_cutoff = now - timedelta(days=end_delay)
        start_cutoff = now - timedelta(days=start_delay)
        stats_table.loc['Total comments', col_name] = len(df_user[(start_cutoff < df_user.timestamp) & (df_user.timestamp <= end_cutoff)])
        stats_table.loc['Total responses', col_name] = sum(df_user.loc[(start_cutoff < df_user.timestamp) & (df_user.timestamp <= end_cutoff), 'received_response'])
        if stats_table.loc['Total comments', col_name] == 0:
            stats_table.loc['Response percentage %', col_name] = 0
        else:
            stats_table.loc['Response percentage %', col_name] = round(100*stats_table.loc['Total responses', col_name] / stats_table.loc['Total comments', col_name])
        stats_table.loc['Total unique fans', col_name] = len(df_user.loc[(start_cutoff < df_user.timestamp) & (df_user.timestamp <= end_cutoff), 'fan_id'].unique())

    def percent_diff(col_1, col_2):
        diff = ((col_1 - col_2) / (0.5*(col_1 + col_2))).apply(lambda x: round(x*100))
        return diff.apply(lambda x: f'+{x}%' if x > 0 else f'{x}%')

    # Add percentage diff
    stats_table['7 - 14 days'] = percent_diff(stats_table['Last 7 days'], stats_table['7 - 14 days'])
    stats_table['14 - 28 days'] = percent_diff(stats_table['Last 14 days'], stats_table['14 - 28 days'])
    stats_table['30 - 60 days'] = percent_diff(stats_table['Last 30 days'], stats_table['30 - 60 days'])

    # Reformat as string
    stats_table['Last 7 days'] = stats_table.apply(lambda row: f"{row['Last 7 days']}  ({row['7 - 14 days']})", axis=1)
    stats_table['Last 14 days'] = stats_table.apply(lambda row: f"{row['Last 14 days']}  ({row['14 - 28 days']})", axis=1)
    stats_table['Last 30 days'] = stats_table.apply(lambda row: f"{row['Last 30 days']}  ({row['30 - 60 days']})", axis=1)

    # Drop un needed rows
    stats_table.drop(columns=['7 - 14 days', '14 - 28 days', '30 - 60 days'], inplace=True)
    stats_table.reset_index(inplace=True)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(stats_table.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[stats_table[col] for col in stats_table.columns],
                fill_color='lavender',
                align='left'))
    ])
    return fig