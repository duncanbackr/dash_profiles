from Backrest.get_creds import create_signed_jwt,exchange_jwt_for_token 
import requests
import json 
from Backrest.get_data import get_creators, get_comments, get_fans, get_videos
from Backrest.get_df import videos_comment_fans_df

def get_raw_data(youtube_channel_id):

    creds = '/Users/eli/Desktop/creator_profiles_yt/backrest_invoke_prod.json' 
    f = open(creds ,) 
    credentials_json = json.load(f) 
    run_service_url = 'https://backrest-q2zw6yb3ha-uc.a.run.app'
    signed_jwt = create_signed_jwt(credentials_json, run_service_url)
    token = exchange_jwt_for_token(signed_jwt)
    df = videos_comment_fans_df(token, youtube_channel_id)

    return df