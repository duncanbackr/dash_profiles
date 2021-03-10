import pandas as pd

from app.Process import features, badges

def get_full_df(df):
    """ 
    Function which adds additional feature and fan badges to raw backrest data.
        
    Parmas: 
        pd.DataFrame with columns ['id', 'timestamp', 'fan_id', 'by_creator', 'parent_comment_id']

    Returns:
        pd.DataFrame with new columns ['cum_count', 'received_response', 'static_badge', 'active_badge']

    """
    
    # Set datetimes
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create custom features
    df['cum_count'] = features.add_cum_count(df[['id', 'timestamp', 'fan_id']])
    df['received_response'] = features.add_received_response(df[['id', 'by_creator', 'parent_comment_id']])

    # Add fan labels
    df['static_badge'] = badges.add_static_badge(df[['id', 'fan_id', 'cum_count']])
    df['active_badge'] = badges.add_active_badge(df[['id', 'fan_id', 'timestamp']])

    return df
