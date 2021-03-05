import pandas as pd
from app.Process.add_active_label import add_active_label
from app.Process.add_response import add_received_response_column
from app.Process.get_delays import get_delays
from app.Process.get_top_fan_cutoff import get_cutoff
from app.Process.cum_count import add_cum_count_column
from app.Process.add_passive_label import add_label, fan_type
from app.Process.metrics import fan_metrics
from app.Process.parser import parse_timestamp
from datetime import datetime,timedelta
import numpy as np

def get_full_df(videos_comment_fans):
    videos_comment_fans = add_cum_count_column(videos_comment_fans)
    videos_comment_fans = add_received_response_column(videos_comment_fans)
    videos_comment_fans = get_delays(videos_comment_fans)
    df_fan_metrics = fan_metrics(videos_comment_fans)
    videos_comment_fans = videos_comment_fans.merge(df_fan_metrics, on = 'account_title', how = 'left')
    cutoff = get_cutoff(df_fan_metrics)
    videos_comment_fans = add_label(videos_comment_fans, cutoff)
    videos_comment_fans = add_active_label(videos_comment_fans, cutoff)
    videos_comment_fans = parse_timestamp(videos_comment_fans)

    return videos_comment_fans

def get_auth_df(df):
    df_auth = df[df.by_creator == True]
    return df_auth

def get_df_user(df):
    df_user = df[df.by_creator == False]
    return df_user