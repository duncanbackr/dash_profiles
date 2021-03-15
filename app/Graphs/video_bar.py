import pandas as pd
import plotly.graph_objects as go
import numpy as np

def get_video_plot():

    full_df = pd.read_csv('full_df.csv')
    df_user = full_df[full_df.by_creator == False]
    
    df_user['topFan'] = df_user["active_badge"] == 'topFan'

    df_bar = (df_user
            .groupby(['video_title'])
            .agg({
                'id':'count',
                'video_likes':'first',
                'video_views':'first',
                'upload_timestamp':'first',
                'topFan':'sum'
                }
            )
            .rename(columns={
                            'id':'total_comments'
                            }
                    )
            )

    # # Calculate other metrics
    df_bar['top_fan_percentage'] = round(100*df_bar['topFan'] / df_bar['total_comments'], 1)
    df_bar['top_fan_percentage_string'] = df_bar['top_fan_percentage'].apply(lambda x: str(x) + '%')
    df_bar['other_comments'] = df_bar['total_comments'] - df_bar['topFan']

    # # Sort vids and grab first 15
    df_bar.sort_values(['upload_timestamp','total_comments'], ascending=False, inplace=True)
    df_bar.reset_index(inplace=True)
    df_bar = df_bar[0:15]

    # # Create list of colors for the labels
    avg_top_fan_rate = df_bar['top_fan_percentage'].median()
    color_list = ['green' if x >= avg_top_fan_rate else 'crimson' for x in df_bar['top_fan_percentage']]

    fig = go.Figure(data=[
        go.Bar(
            name='Other Fans',
            x=df_bar.video_title,
            y=df_bar.other_comments),
        go.Bar(
            name='Top Fans',
            x=df_bar.video_title,
            y=df_bar.topFan,
            text=df_bar.top_fan_percentage_string,
            textposition='outside',
            marker= {'color':'lightblue'},
            textfont=dict(
                size=14,
                color=color_list)
            )
        ])

    fig.update_layout(title='Videos with the most fan activity',
                    xaxis_title='Videos',
                    yaxis_title='Total comments')

    #fig.update_xaxes(showticklabels=False)
    fig.update_layout(barmode='stack')
    fig['layout'].update(width=1500, height=700, autosize=False)

    return fig