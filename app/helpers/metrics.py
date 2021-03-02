import pandas as pd

def fan_metrics(df_user):

    if 'cum_count' not in df_user.columns:
        df_user = add_received_response_column(df_user)

        df_user = df_user[df_user.by_creator == False]
        
        df_user = add_cum_count_column(df_user)

    
    df_fan_metrics = (df_user.groupby(['account_title']).agg({
                'timestamp':'unique',
                'id':'count',
                'video_title': 'unique',
                'received_response':'sum'
                })
                .rename(columns={
                            'id':'total_comments',
                            'timestamp':'unique_dates_commented_on',
                            'video_title':'unique_video_commented_on',
                            'received_response':'creator_responses'
                            })
                )
    return df_fan_metrics