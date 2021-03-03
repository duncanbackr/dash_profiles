from Backrest.get_data import get_videos, get_comments, get_fans
import json 
from Backrest.get_creds import exchange_jwt_for_token, create_signed_jwt
import pandas as pd
from Process.add_active_label import add_active_label
from Process.add_response import add_received_response_column
from Process.get_delays import get_delays
from Process.get_top_fan_cutoff import get_cutoff
from Process.cum_count import add_cum_count_column
from Process.add_passive_label import add_label, fan_type
from Backrest.get_df import videos_comment_fans_df
from Process.metrics import fan_metrics
from Process.parser import parse_timestamp
from datetime import datetime,timedelta
import numpy as np

creds = '/Users/eli/Desktop/creator_profiles_yt/backrest_invoke_prod.json' 
f = open(creds ,) 
credentials_json = json.load(f) 
run_service_url = 'https://backrest-q2zw6yb3ha-uc.a.run.app'
signed_jwt = create_signed_jwt(credentials_json, run_service_url)
token = exchange_jwt_for_token(signed_jwt)


def get_full_df(token, platform_account_id):
    videos_comment_fans = videos_comment_fans_df(token, platform_account_id)
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

def get_auth_df(token, platform_account_id):
    df = get_full_df(token, platform_account_id)
    df_auth = df[df.by_creator == True]
    return df_auth

def get_df_user(token, platform_account_id):
    df = get_full_df(token, platform_account_id)
    df_user = df[df.by_creator == False]
    return df_user