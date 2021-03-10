import pandas as pd

def add_received_response_column(df):
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