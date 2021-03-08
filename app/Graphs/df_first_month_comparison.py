
import plotly.graph_objects as go
import pandas as pd 

def create_video_comparison(df_user):
    df_video_comparison = df_user[['by_creator', 'video_title', 'timestamp', 'upload_timestamp']]


    # Calculate diff between video timestamp and comment timestamp as Timedelta and fraction
    df_video_comparison['time_delta'] = df_video_comparison.timestamp - pd.to_datetime(df_video_comparison.upload_timestamp).dt.tz_localize(None)
    df_video_comparison['time_delta_fraction'] = df_video_comparison.time_delta.apply(lambda x: x.days + x.seconds/86400)

    # Remove time deltas that are negative (caused as a result of time zone errors)
    df_video_comparison = df_video_comparison.loc[( 0 < df_video_comparison.time_delta_fraction ) & ( df_video_comparison.time_delta_fraction < 30)]

    # # Sort and find Cumulative Sum
    df_video_comparison.sort_values('time_delta', inplace=True)
    df_video_comparison['cumsum'] = 1
    df_video_comparison['cumsum'] = df_video_comparison.groupby('video_title')['cumsum'].cumsum()

    return df_video_comparison

def fig_video_comparison(df_user):

    df_video_timeline = create_video_comparison(df_user)

    titles_sorted = (df_video_timeline
                    .sort_values('upload_timestamp', ascending=False)
                    .video_title
                    .unique()
                    )

    fig = go.Figure()

    for title in titles_sorted:
        temp_data = df_video_timeline.loc[df_video_timeline.video_title == title]
        fig.add_trace(
            go.Scatter(
                x=temp_data["time_delta_fraction"], 
                y=temp_data["cumsum"],
                mode='lines',
                name=title
                )
        )
        
        fig.add_trace(
            go.Scatter(
                x=temp_data.loc[temp_data.by_creator == True, "time_delta_fraction"],
                y=temp_data.loc[temp_data.by_creator == True, "cumsum"],
                mode='markers',
                name='Responses By Creator: ' + title,
                marker={'color':'gold', 'line':{'color':'black', 'width':1}}
        ))

    fig.update_layout(title='Comments over time increase due to creator responses',
                    xaxis_title='Days since video post',
                    yaxis_title='Total comments')

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    return fig