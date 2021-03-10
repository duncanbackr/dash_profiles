import pandas as pd

def add_cum_count(df):
    """ 
    Function which calculates cumulative comment count for each fan

    Params: 
        pd.DataFrame with columns: ['id', 'timestamp', 'fan_id']
    
    Returns:
        pd.Series with column ['cum_count']
    """

    df.sort_values('timestamp', inplace=True)
    df.loc['cum_count'] = 1
    cum_count = df.groupby('fan_id')['cum_count'].cumsum()
    return cum_count

def add_received_response(df):
    """ 
    Functions which checks if creator responded to the a comment

    Params:
        pd.Dataframe with columns ['id', 'by_creator', 'parent_comment_id']

    Returns:
        pd.Series with booleans

    """

    responded_comments = set(df.loc[df['by_creator'] == True, 'parent_comment_id'])
    received_response = df.id.apply(lambda x: x in responded_comments)
    return received_response

