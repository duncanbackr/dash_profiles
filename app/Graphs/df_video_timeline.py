
import plotly.graph_objects as go

def create_video_timeline(df_user):
    df_video_timeline = df_user[['by_creator', 'video_title', 'timestamp', 'upload_timestamp']]

    # Sort and find Cumulative Sum
    df_video_timeline.sort_values('timestamp', inplace=True)
    df_video_timeline['cumsum'] = 1
    df_video_timeline['cumsum'] = df_video_timeline.groupby('video_title')['cumsum'].cumsum()

    return df_video_timeline

def fig_video_timeline(df_user):

    df_video_timeline = create_video_timeline(df_user)

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
                x=temp_data["timestamp"], 
                y=temp_data["cumsum"],
                mode='lines',
                name=title
                )
        )
        
        fig.add_trace(
            go.Scatter(
                x=temp_data.loc[temp_data.by_creator == True, "timestamp"],
                y=temp_data.loc[temp_data.by_creator == True, "cumsum"],
                mode='markers',
                name='Responses By Creator: ' + title,
                marker={'color':'gold', 'line':{'color':'black', 'width':1}}
        ))

    fig.update_layout(title='Comments over time per video',
                    xaxis_title='Date',
                    yaxis_title='Total comments')

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    return fig
