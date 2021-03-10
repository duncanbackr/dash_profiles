import pandas as pd

from app.Process import features, badges

def get_full_df(df):
    
    # Set datetimes
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['upload_timestamp'] = pd.to_datetime(df.upload_timestamp)

    # Create custom features
    df['cum_count'] = features.add_cum_count(df[['id', 'timestamp', 'fan_id']])
    df['received_response'] = features.add_received_response(df[['id', 'by_creator', 'parent_comment_id']])

    # Add fan labels
    df['static_label'] = badges.add_static_badge(df[['id', 'fan_id', 'cum_count']])
    df['active_label'] = badges.add_active_badge(df[['id', 'fan_id', 'timestamp']])

    return df
