import numpy as np
import pandas as pd
def add_active_label(df_comments_fans_videos, top_fan_cutoff):
    df_comments_fans_videos['active_label'] = np.nan
    df_comments_fans_videos.loc[df_comments_fans_videos['total_comments'] == 1,'active_label'] = 'newFan'
    df_comments_fans_videos.loc[df_comments_fans_videos['delay2'] < 7,'active_label'] = 'trendingFan'
    df_comments_fans_videos.loc[(df_comments_fans_videos['delay2'] >= 30) & (df_comments_fans_videos['delay1'] < 14),'active_label'] = 'reEngageFan'
    df_comments_fans_videos.loc[df_comments_fans_videos['total_comments'] > top_fan_cutoff,'active_label'] = 'topFan'
    return df_comments_fans_videos