import requests
import json

from config import Config
from app.Backrest import authentication
from app.Backrest.get_df import videos_comment_fans_df

def get_raw_data(youtube_channel_id):

    token = authentication.get_token(Config.BACKREST_URL)
    
    df = videos_comment_fans_df(token, youtube_channel_id)

    return df