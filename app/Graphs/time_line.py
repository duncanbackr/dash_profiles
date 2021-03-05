import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def df_time_user(df_user):

    df_fan_posts = (df_user.groupby(['hours' ])["video_title"]
                    .count()
                    .reset_index()
                    )

    return df_fan_posts


def df_time_auth(df_user):

    df_auth = df_user[df_user['by_creator'] == True]

    df_fan_posts = (df_user.groupby(['hours' ])["video_title"]
                    .count()
                    .reset_index()
                    )

    df_auth_post = (df_auth['hours']
                    .value_counts()
                    .reindex(df_fan_posts['hours' ]
                    .unique(), fill_value=0)
                    .to_frame()
                    )

    df_auth_post['time'] = df_auth_post.index   

    df_auth_post = df_auth_post.dropna()

    return df_auth_post


def fig_time(df_fan_posts, df_auth_post):

    ############create 3 plots for each timezone##########
    df_fan_posts['hours-ON'] = np.arange(19,24).tolist()+ np.arange(0,19).tolist()
    df_auth_post['hours-ON'] = np.arange(19,24).tolist()+ np.arange(0,19).tolist()
    df_fan_posts['hours-BC'] = np.arange(17,24).tolist()+ np.arange(0,17).tolist()
    df_auth_post['hours-BC'] = np.arange(17,24).tolist()+ np.arange(0,17).tolist()
    df_fan_posts['hours-NS'] = np.arange(15,24).tolist()+ np.arange(0,15).tolist()
    df_auth_post['hours-NS'] = np.arange(15,24).tolist()+ np.arange(0,15).tolist()

    #############sort dataframe by timezone###########
    all_time_NY = df_fan_posts.sort_values(by ='hours-ON')
    all_time_NY_auth = df_auth_post.sort_values(by ='hours-ON')
    all_time_CA = df_fan_posts.sort_values(by ='hours-BC')
    all_time_CA_auth = df_auth_post.sort_values(by ='hours-BC')
    all_time_NS = df_fan_posts.sort_values(by ='hours-NS')
    all_time_NS_auth = df_auth_post.sort_values(by ='hours-NS')

    fig_time = make_subplots(specs=[[{"secondary_y": True}]])

    fig_time.add_trace(
    go.Line(
        x=all_time_NY['hours-ON'], 
        y=all_time_NY['video_title'], 
        mode='lines', 
        name="# of Fan Comments - ON"),
    secondary_y=False,
    )

    fig_time.add_trace(
    go.Line(
        x=all_time_CA['hours-BC'], 
        y=all_time_CA['video_title'], 
        mode='lines', 
        name="# of Fan Comments - BC"),
    secondary_y=False,
    )

    fig_time.add_trace(
    go.Line(
        x=all_time_NS['hours-NS'], 
        y=all_time_NS['video_title'], 
        mode='lines', 
        name="# of Fan Comments - NS"),
    secondary_y=False,
    )

    fig_time.add_trace(
    go.Scatter(
        x=all_time_NY_auth['hours-ON'], 
        y=all_time_NY_auth['hours'], 
        mode='lines', 
        name="# of Creator Comments - ON"),
    secondary_y=True,   
    )

    fig_time.add_trace(
    go.Scatter(
        x=all_time_CA_auth['hours-BC'], 
        y=all_time_CA_auth['hours'], 
        mode='lines', 
        name="# of Creator Comments - BC"),
    secondary_y=True,   
    )

    fig_time.add_trace(
    go.Scatter(
        x=all_time_NS_auth['hours-NS'], 
        y=all_time_NS_auth['hours'], 
        mode='lines', 
        name="# of Creator Comments - NS"),
    secondary_y=True,   
    )

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="ON TZ",
                        method="update",
                        args=[{"visible": [True, False, False, True, False, False]},
                                ]),
                    dict(label="BC TZ",
                        method="update",
                        args=[{"visible": [False, True, False, False, True, False]},
                                ]),
                    dict(label="NS TZ",
                        method="update",
                        args=[{"visible": [False, False, True, False, False, True]},
                                ]),
                ]),
            )
        ])


    fig_time.update_layout(
    title_text="Comments Posted by Hour of the Day", xaxis = dict(
        tickmode = 'array',
        tickvals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        ticktext = ['12am', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm','11pm']
        )
    )
    fig_time.update_xaxes(title_text="Hour of Day")
    fig_time.update_yaxes(title_text="# of Fan Comments", secondary_y=False)
    fig_time.update_yaxes(title_text="# of Creator Comments", secondary_y=True)

    fig_time.update_layout(
    yaxis=dict(
        title="# of Fan Comments",
        titlefont=dict(
            color="blue"
        ),
    ),

    yaxis2=dict(
        title="# of Creator Comments",
        titlefont=dict(
            color="crimson"
        ),
        side="right"
    ),
    )

    fig_time.update_xaxes(showgrid=False, zeroline=False)
    fig_time.update_yaxes(showgrid=False, zeroline=False)

    return fig_time