import pandas as pd
import numpy as np

def get_top_fan_cutoff(df):
    """ Calculates topfan cuttoff as two standard deviations above mean fan comment count """
    
    # Because have no fan_id they will not be included in the count
    fan_comments_mean = np.mean(df.groupby('fan_id')['id'].count())
    fan_comments_std = np.std(df.groupby('fan_id')['id'].count())

    top_fan_cutoff = fan_comments_mean + 2*fan_comments_std    
    
    if top_fan_cutoff > 3:
        return top_fan_cutoff
    
    return 3

def add_static_badge(df):
    """ 
    Calculates static badge for each row

    Params:
        pd.DataFrame(columns = ['id', 'fan_id', 'cum_count'])

    Returns:
        pd.Series with column 'Static_badge'

    """
    top_fan_cutoff = get_top_fan_cutoff(df)

    def fan_type(x, top_fan_cutoff):
        if x == 1:
            return 'newFan'
        elif (x > 1) & (x < top_fan_cutoff):
            return 'trendingFan'
        else:
            return 'topFan' 
    
    static_badge = df.cum_count.apply(lambda x: fan_type(x, top_fan_cutoff))

    return static_badge

def add_active_badge(df):
    """ 
    Calculates active badge for each row

    Params:
        pd.DataFrame(columns = ['id', 'fan_id', 'timestamp'])

    Returns:
        pd.Series with column 'active_badge'

    """

    top_fan_cutoff = get_top_fan_cutoff(df)

    fan_group = df.groupby('fan_id')['timestamp']

    fan_metrics = pd.DataFrame()
    fan_metrics['total_comments'] = fan_group.count()
    fan_metrics['delay1'] = (pd.Timestamp.utcnow() - fan_group.max()).dt.days
    fan_metrics['delay2'] = (pd.Timestamp.utcnow() - fan_group.apply(lambda x: x.nlargest(2).min())).dt.days

    def active_fan_calculation(total_comments, delay1, delay2):
        if total_comments == 1:
            return 'newFan'
        elif total_comments >= top_fan_cutoff:
            return 'topFan'
        elif delay2 < 14:
            return 'trendingFan'
        elif (delay1 < 14) & (delay2 >= 30):
            return 'reEngagedFan'
        else:
            return 'other'

    fan_metrics['active_badge'] = fan_metrics.apply(
        lambda row: active_fan_calculation(
            total_comments=row['total_comments'],
            delay1=row['delay1'],
            delay2=row['delay2']
            ),
        axis=1
        )

    active_badge = df.join(fan_metrics, on='fan_id')['active_badge']
    return active_badge




