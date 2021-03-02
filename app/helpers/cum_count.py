import pandas as pd 

def add_cum_count_column(df_comments_fans_videos):
    df_comments_fans_videos.sort_values('timestamp', inplace=True)
    df_comments_fans_videos['cum_count'] = 1
    df_comments_fans_videos['cum_count'] = df_comments_fans_videos.groupby('account_title')['cum_count'].cumsum()
    return df_comments_fans_videos