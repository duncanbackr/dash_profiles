from helpers.get_data import get_videos, get_comments, get_fans
import json 
from helpers.get_creds import exchange_jwt_for_token, create_signed_jwt
import pandas as pd
from helpers.add_active_label import add_active_label
from helpers.add_response import add_received_response_column
from helpers.get_delays import get_delays
from helpers.get_top_fan_cutoff import get_cutoff
from helpers.cum_count import add_cum_count_column
from helpers.add_passive_label import add_label, fan_type
from helpers.get_df import videos_comment_fans_df
from helpers.metrics import fan_metrics
from helpers.parser import parse_timestamp
from datetime import datetime,timedelta
from helpers import get_full_df

creds = '/Users/eli/Desktop/creator_profiles_yt/backrest_invoke_prod.json' 
f = open(creds ,) 
credentials_json = json.load(f) 
run_service_url = 'https://backrest-q2zw6yb3ha-uc.a.run.app'
signed_jwt = create_signed_jwt(credentials_json, run_service_url)
token = exchange_jwt_for_token(signed_jwt)


if __name__ == '__main__':
    df = get_full_df(token, 'UCN_fKex8H7MgZiPPzRhgg0A')
    print(df.head())