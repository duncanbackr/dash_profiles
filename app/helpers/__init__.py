from get_data import get_videos, get_comments, get_fans
import json 
from get_creds import exchange_jwt_for_token, create_signed_jwt
import pandas as pd
from add_active_label import add_active_label
from add_response import add_received_response_column
from get_delays import get_delays
from get_top_fan_cutoff import get_cutoff
from cum_count import add_cum_count_column
from add_passive_label import add_label, fan_type
from get_df import videos_comment_fans_df
from metrics import fan_metrics
from datetime import datetime,timedelta

creds = '/Users/eli/Desktop/creator_profiles_yt/backrest_invoke_prod.json' 
f = open(creds ,) 
credentials_json = json.load(f) 
run_service_url = 'https://backrest-q2zw6yb3ha-uc.a.run.app'
signed_jwt = create_signed_jwt(credentials_json, run_service_url)
token = exchange_jwt_for_token(signed_jwt)


def get_full_df(token, platform_account_id):
    videos_comment_fans_df = videos_comment_fans_df(token, platform_account_id)
    videos_comment_fans_df = add_cum_count_column(videos_comment_fans_df)
    videos_comment_fans_df = add_received_response_column(videos_comment_fans_df)
    videos_comment_fans_df = get_delays(videos_comment_fans_df)
    df_fan_metrics = fan_metrics(videos_comment_fans_df)
    videos_comment_fans_df = videos_comment_fans_df.merge(df_fan_metrics, on = 'account_title', how = 'left')
    videos_comment_fans_df = add_active_label(videos_comment_fans_df)
    cutoff = get_cutoff(df_fan_metrics)
    videos_comment_fans_df = add_passive_label(videos_comment_fans_df, cutoff)

    return videos_comment_fans_df 


