import pandas as pd
import plotly.graph_objects as go

def get_figure():

    full_df = pd.read_csv('full_df.csv')
    full_df.timestamp = pd.to_datetime(full_df.timestamp)
    df_user = full_df[full_df.by_creator == False]
    df_auth = full_df[full_df.by_creator == True]


    # Create ordered Data Frame]
    day_dict = {6:'Sun', 0:'Mon', 1:'Tues', 2:'Wed', 3:'Thurs', 4:'Fri', 5:'Sat'}
    df_days = pd.DataFrame(index=day_dict.values())

    # Fill values for total and creator comments
    df_user['day'] = df_user.timestamp.apply(lambda x: day_dict[x.weekday()])
    df_auth['day'] = df_auth.timestamp.apply(lambda x: day_dict[x.weekday()])
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