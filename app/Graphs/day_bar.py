import pandas as pd
import plotly.graph_objects as go

def fig_day(df_user, df_auth):


    # Create ordered Data Frame
    df_days = pd.DataFrame(index=['Sun', 'Mon', 'Tues', 'Wed','Thurs', 'Fri', 'Sat'])

    # Fill values for total and creator comments
    df_days['total_comments'] = df_user.groupby('day')["video_title"].count()
    df_days['creator_comments'] = df_auth.groupby('day')["video_title"].count()
    df_days.fillna(0, inplace=True)

    # Create Figure    
    fig_day = go.Figure(
        data=[
            go.Bar(
                name='Fan',
                x=df_days.index,
                y=df_days['total_comments'],
                yaxis='y',
                offsetgroup=1
                ),
            go.Bar(
                name='Creator',
                x=df_days.index,
                y=df_days['creator_comments'],
                yaxis='y2',
                offsetgroup=2
                )
            ],
        layout={
            'yaxis': {'title': 'Fan Comments'},
            'yaxis2': {
                'title': 'Creator Comments',
                'overlaying': 'y',
                'side': 'right'
                }
            }
        )

    # Change the bar mode
    fig_day.update_layout(title_text="Comments Posted by Day of the Week", barmode='group')

    # Updating axis color and titles
    fig_day.update_xaxes(title_text="Days of the Week")
    fig_day.update_layout(
        yaxis=dict(
            title="Fan Comments",
            titlefont=dict(
                color="blue"
                ),
            ),
        yaxis2=dict(
            title="Creator Comments",
            titlefont=dict(
                color="crimson"
                ),
            side="right"
            )
        )

    fig_day.update_xaxes(showgrid=False, zeroline=False)
    fig_day.update_yaxes(showgrid=False, zeroline=False)
    return fig_day