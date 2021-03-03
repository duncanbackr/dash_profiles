import pandas as pd
import plotly.graph_objects as go
import numpy as np

def get_video_plot(df_user):

    df_bar = df_user[['id', 'video_like_count','video_view_count','video_title', 'active_label', 'upload_timestamp']]

    # top fans boolean
    df_bar['fan_type_bool'] = df_bar["active_label"].replace({
                                                        np.NaN:False,
                                                        'newFan':False,
                                                        'topFan':True,
                                                        'trendingFan':False,
                                                        'reEngageFan':False
                                                        })

    Option2 = (df_bar
            .groupby(['video_title'])
            .agg({
                'id':'count',
                'video_like_count':'first',
                'video_view_count':'first',
                'upload_timestamp':'first',
                'fan_type_bool':'sum'
                }
                )
            .rename(columns={
                            'id':'total_comments',
                            'fan_type_bool':'top_fan_comments'
                            }
                    )
            )

    # # Calculate other metrics
    Option2['top_fan_percentage'] = round(100*Option2['top_fan_comments'] / Option2['total_comments'], 1)
    Option2['top_fan_percentage_string'] = Option2['top_fan_percentage'].apply(lambda x: str(x) + '%')
    Option2['other_comments'] = Option2['total_comments'] - Option2['top_fan_comments']

    # # Sort vids and grab first 15
    Option2.sort_values(['upload_timestamp','total_comments'], ascending=False, inplace=True)
    Option2.reset_index(inplace=True)
    Option2 = Option2[0:15]

    # # Create list of colors for the labels
    avg_top_fan_rate = Option2['top_fan_percentage'].median()
    color_list = ['green' if x >= avg_top_fan_rate else 'crimson' for x in Option2['top_fan_percentage']]

    fig = go.Figure(data=[
        go.Bar(
            name='Other Fans',
            x=Option2.video_title,
            y=Option2.other_comments),
        go.Bar(
            name='Top Fans',
            x=Option2.video_title,
            y=Option2.top_fan_comments,
            text=Option2.top_fan_percentage_string,
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