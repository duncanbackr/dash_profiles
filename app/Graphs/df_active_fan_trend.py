import pandas as pd
import plotly.graph_objects as go
from fbprophet import Prophet
from plotly.subplots import make_subplots

def activeFans_fig(df_user):

    # Fans Dataframe
    df_fans = df_user[['id', 'dates', 'account_title', 'by_creator', 'parent_youtube_comment_id']]
    df_fans = df_fans.loc[df_fans.by_creator == False]

    # Create Daily active Fans table
    min_date = df_fans.dates.min()
    date_index = pd.date_range(start=min_date, end=pd.datetime.now(), freq='D')
    active_fans = pd.DataFrame(index=date_index)
    active_fans['daily_active'] = df_fans.groupby('dates')['account_title'].nunique()
    active_fans['daily_responses'] = df_fans.groupby('dates')['parent_youtube_comment_id'].nunique()
    active_fans.fillna(0, inplace=True)

    # Calculate rolling sums
    active_fans['weekly_active'] = active_fans['daily_active'].rolling(7, min_periods=1).sum()
    active_fans['bi_weekly_active'] = active_fans['daily_active'].rolling(14, min_periods=1).sum()
    active_fans['monthly_active'] = active_fans['daily_active'].rolling(28, min_periods=1).sum()
    active_fans['monthly_responses'] = active_fans['daily_responses'].rolling(28, min_periods=1).sum()
    active_fans['monthly_avg'] = active_fans['monthly_active'].ewm(com=4).mean() # Exponentially waited mean
    active_fans['monthly_responses_avg'] = active_fans['monthly_responses'].ewm(com=4).mean()
    # Video posts dataframe
    video_post_dates = df_user.upload_timestamp.unique().date
    active_fans['video_posted'] = False
    active_fans.loc[video_post_dates, 'video_posted'] = True
    video_posts_df = active_fans.loc[active_fans.video_posted].reset_index()

    #### FB PROPHET ####

    # Use fb prophet to generate trend line
    m = Prophet()
    #m.add_regressor('video_posted') # Add video post as input
    prophet_data = active_fans.reset_index()[['index', 'monthly_active','video_posted']]
    prophet_data = prophet_data.rename(columns={'index':'ds', 'monthly_active':'y'})
    m.fit(prophet_data)
    future = m.make_future_dataframe(periods=60)
    #future = future.join(active_fans['video_posted'], on = 'ds').fillna(False)
    trend = m.predict(future)


    #### PLOT FIGURE #####

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Monthly and Daily data
    fig.add_trace(
        go.Scatter(
            x=trend['ds'],
            y=trend['yhat_lower'],
            fill=None,
            mode='lines',
            line_color='lightblue',
            name='Lower estimate'
            ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=trend['ds'],
            y=trend['yhat_upper'],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            line_color='lightblue',
            name='Upper estimate'
            ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=active_fans.index, 
            y=active_fans['monthly_avg'],
            mode='lines',
            name='Monthly Average'
            ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=active_fans.index, 
            y=active_fans['monthly_responses_avg'],
            mode='lines',
            name='Monthly Responses Average'
            ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            x=active_fans.index, 
            y=active_fans['monthly_active'],
            mode='markers',
            marker={'color':'black', 'size':4},
            name='Monthly'
            ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=active_fans.index, 
            y=active_fans['daily_active'],
            mode='lines',
            name='Daily'
            ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=active_fans.loc[active_fans.video_posted].index, 
            y=active_fans.loc[active_fans.video_posted]['daily_active'],
            mode='markers',
            marker={'color':'red', 'size':4},
            name='Video Posted'
            ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=trend['ds'], 
            y=trend['trend'],
            mode='lines',
            marker={'color':'darkblue'},
            name='Trend'
            ),
        secondary_y=False,)
        
    
    fig.update_layout(title='Monthly Active Fans',
                    xaxis_title='Date',
                    yaxis_title='Number of active fans')

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(title_text="# of Active Fans", secondary_y=False)
    fig.update_yaxes(title_text="# of Creator Responses", secondary_y=True)

    return fig