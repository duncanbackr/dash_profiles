from datetime import datetime, timezone
import pandas as pd

def delay_1(df):
    """ 
    Calculates delay between todays date and comment date in units of days
    """
    
    now_utc = pd.Timestamp.utcnow()
    delay1 = (now_utc - df['timestamp']).dt.days + (now_utc - df['timestamp']).dt.seconds/3600
    return delay1


def get_delays(df_comments_fans_videos):


    df_comments_fans_videos['timestamp'] = pd.to_datetime(df_comments_fans_videos['timestamp'])
    df_sec_date = df_comments_fans_videos.groupby('fan_id')['timestamp'].apply(lambda x: x.nsmallest(2)).rename({'timestamp':'second_date'})

    df_comments_fans_videos = df_comments_fans_videos.merge(df_sec_date, how='left', on = 'fan_id')

    df_comments_fans_videos.rename(columns={'timestamp_x':'timestamp','timestamp_y':'second_date_posted' }, inplace=True)
    df_comments_fans_videos['timestamp'] = pd.to_datetime(df_comments_fans_videos['timestamp'].dt.tz_localize(None))
    df_comments_fans_videos['second_date_posted'] = pd.to_datetime(df_comments_fans_videos['second_date_posted'].dt.tz_localize(None))

    today = pd.to_datetime(datetime.now())
    df_comments_fans_videos['delay1'] = (today - df_comments_fans_videos['timestamp']).dt.days + ((today - df_comments_fans_videos['timestamp']).dt.seconds)/3600
    df_comments_fans_videos['delay2'] = (today - df_comments_fans_videos['second_date_posted']).dt.days + ((today - df_comments_fans_videos['second_date_posted']).dt.seconds)/3600

    return df_comments_fans_videos