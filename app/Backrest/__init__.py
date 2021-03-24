import requests
import json
import pandas as pd

from config import Config
from app.Backrest import authentication
from app.Backrest import request

def get_raw_data(youtube_channel_id:str):
    """ 
        Function which returns all backrest data for a creator as a single dataframe.
        
    Parmas: 
        youtube_channel_id: str

    Returns:
        pd.DataFrame(
            columns=['id', 'by_creator', 'backr_reply', 'parent_comment_id', # Comment info
                    'video_id', 'video_title', 'upload_timestamp', 'video_views', 'video_likes', # Video info
                    'fan_id', 'account_title' # Fan info
                    ]
        )
    """

    token = authentication.get_token(Config.BACKREST_URL)
    
    videos = pd.DataFrame(
        request.get_resource(
            resource='/v1/youtube/videos/', 
            params={'creator__youtube_platform_account_id': youtube_channel_id,
                    'limit':1000},
            token=token,
        )
    )

    fans = pd.DataFrame(
        request.get_resource(
            resource='/v1/youtube/fans/', 
            params={'creator__youtube_platform_account_id': youtube_channel_id,
                    'limit':10000},
            token=token,
        )
    )

    comments = pd.DataFrame(
        request.get_resource(
            resource='/v1/youtube/comments/',
            params={'youtube_video__creator__youtube_platform_account_id': youtube_channel_id,
                'limit':15000},
            token=token,
        )
    )

    df = (
        comments
        .merge(
            videos,
            how='left',
            left_on='video',
            right_on='url',
            suffixes=['_comment', '_video'])
        .merge(
            fans,
            how='left',
            left_on='fan',
            right_on='url',
            suffixes=['_comment', '_fan']
        )
        .rename(columns={
            'url_comment': 'id',
            'url_video': 'video_id',
            'fan': 'fan_id',
            'parent_comment': 'parent_comment_id',
            'title': 'video_title',
            'uploaded': 'upload_timestamp',
            'youtube_channel_name': 'account_title',
            'created': 'timestamp',
            'views': 'video_views',
            'likes_video': 'video_likes'
        })
    )

    columns = ['id', 'by_creator', 'backr_reply', 'parent_comment_id', 'timestamp', # Comment info
               'video_id', 'video_title', 'upload_timestamp', 'video_views', 'video_likes', # Video info
               'fan_id', 'account_title' # Fan info
               ]

    return df[columns]