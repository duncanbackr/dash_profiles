import numpy as np
import pandas as pd
import plotly.express as px


def create_bubble_data(df_user):

    # Calculate the agregations
    df_bubble = df_user[['id', 'by_creator', 'video_title', 'video_view_count', 'upload_timestamp']]
    df_bubble = (df_bubble
                .groupby('video_title')
                .agg({'id': 'count',
                      'by_creator': 'sum',
                      'video_view_count': 'first',
                      'upload_timestamp': 'first'
                      }
                    )
                )
              
    df_bubble = df_bubble.rename(columns={'id': 'total_comments',
                                          'by_creator': 'total_responses'
                                          })
    df_bubble['engagment_score'] = (df_bubble.total_comments*df_bubble.total_comments)/ df_bubble.video_view_count
    
    # comment size between 10 and 50 for better visisbility
    c = df_bubble['total_comments']
    df_bubble['bubble_size'] = ((c-c.min()) / (c.max()-c.min()))* 55 + 5

    # Sort by date video was posted
    titles_sorted = (df_user
                    .sort_values('upload_timestamp', ascending=False)
                    .video_title
                    .unique()
                    )
    df_bubble = pd.DataFrame(index=titles_sorted).join(df_bubble)
    df_bubble = df_bubble.reset_index().rename(columns={'index':'video_title'})
    df_bubble = df_bubble[df_bubble['total_responses'] > 0]
    df_bubble = df_bubble.sort_values(by=['total_responses'])
    #df_bubble['Response:Comments Ratio'] = df_bubble['total_responses']/df_bubble['total_comments']

    # Round the data
    df_bubble = df_bubble.round(2)

    return df_bubble


def bubble_fig(df_user):

    df_bubble = create_bubble_data(df_user)

    c = np.mean(df_bubble['engagment_score'])/ np.mean(df_bubble['total_responses'])
    x = df_bubble['total_responses']
    y = df_bubble['engagment_score']

    #if x is not empy
    p = np.polyfit(x, y, 1)
    fit_line = x*p[0] + p[1]

    fig_bubble = px.scatter(df_bubble, 
                            x=x, 
                            y=y,
                            size="bubble_size",
                            color="video_title",
                            size_max=50,
                            hover_data=['total_responses', 'total_comments', 'video_view_count', 'engagment_score'],
                            labels={
                                "total_responses": "Creator Responses",
                                "engagment_score": "Engagement Rate",
                                "total_comments": "Total comments",
                                "video_view_count": "Total views"
                                },
                            title="Responses Vs Engagement Rate, bubble size is total video comments"
                            )

    fig2 = px.line(x=x, y=fit_line)
    fig_bubble.append_trace(fig2.data[0],None,None)
    fig_bubble.update_xaxes(showticklabels=True)
    fig_bubble.update_yaxes(showticklabels=False)
    fig_bubble.update_xaxes(showgrid=False, zeroline=False)
    fig_bubble.update_yaxes(showgrid=False, zeroline=False)

    fig_bubble.update_layout(xaxis_title="Number of Responses", yaxis_title="Engagement Score (C^2/V)")
    
    return fig_bubble