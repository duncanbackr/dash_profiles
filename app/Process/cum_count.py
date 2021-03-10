import pandas as pd

def add_cum_count_column(df):
    """ 
    Function which calculates cumulative comment count for each fan

    Params: 
        pd.DataFrame with columns: ['id', 'timestamp', 'fan_id']
    
    Returns:
        pd.Series with column ['cum_count']
    """

    df.sort_values('timestamp', inplace=True)
    df['cum_count'] = 1
    cum_count = df.groupby('fan_id')['cum_count'].cumsum()
    return cum_count
