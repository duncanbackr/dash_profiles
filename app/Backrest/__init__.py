import requests
import json

from config import Config
from Backrest import authentication
from Backrest.get_df import videos_comment_fans_df

def get_raw_data(youtube_channel_id):

    token = authentication.get_token(Config.BACKREST_URL)
    
    df = videos_comment_fans_df(token, youtube_channel_id)

    return df