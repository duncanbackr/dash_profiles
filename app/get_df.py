from get_data import get_videos, get_comments, get_fans
import json 
from get_creds import exchange_jwt_for_token, create_signed_jwt
import pandas as pd

creds = '/Users/eli/Desktop/creator_profiles_yt/backrest_invoke_prod.json' 
f = open(creds ,) 
credentials_json = json.load(f) 
run_service_url = 'https://backrest-q2zw6yb3ha-uc.a.run.app'
signed_jwt = create_signed_jwt(credentials_json, run_service_url)
token = exchange_jwt_for_token(signed_jwt)

def videos_comment_fans_df(token, platform_account_id):
    df_videos = pd.DataFrame(get_videos(token, platform_account_id))
    df_comments = pd.DataFrame(get_comments(token, platform_account_id))
    df_fans = pd.DataFrame(get_fans(token, platform_account_id))


    df_comments.fan = df_comments.fan.str.split('/')
    df_comments.fan = df_comments.fan.str[-2]

    df_comments.url = df_comments.url.str.split('/')
    df_comments.url = df_comments.url.str[-2]

    df_fans.url = df_fans.url.str.split('/')
    df_fans.url = df_fans.url.str[-2]

    df_comments_and_fans = pd.merge(df_comments, df_fans, left_on = 'fan', right_on = 'url', how = 'left')

    df_comments_and_fans.video = df_comments_and_fans.video.str.split('/')
    df_comments_and_fans.video = df_comments_and_fans.video.str[-2]

    df_videos.url = df_videos.url.str.split('/')
    df_videos.url = df_videos.url.str[-2]

    df_comments_fans_videos = pd.merge(df_comments_and_fans, df_videos, left_on = 'video', right_on = 'url', how = 'left')

    columns_list = ['url_x','archived', 'backr_reply', 'by_creator', 'content', 'created',
       'downvote', 'fan', 'likes_x', 'parent_comment', 'upvote', 'video',
       'youtube_comment_id', 'youtube_channel_id',
       'youtube_channel_name', 'creator_y', 'likes_y',
       'title', 'uploaded', 'views', 'youtube_video_id']

    df_comments_fans_videos = df_comments_fans_videos[columns_list]

    df_comments_fans_videos.parent_comment = df_comments_fans_videos.parent_comment.str.split('/')
    df_comments_fans_videos.parent_comment = df_comments_fans_videos.parent_comment.str[-2]
    df_comments_fans_videos.columns = ['id', 'archived', 'backr_reply', 'by_creator', 'text', 'timestamp', 'downvote', 'fan_id', 'comment_likes', 
              'parent_comment_id', 'upvote', 'video_id', 'youtube_comment_id', 'youtube_channel_id', 'account_title', 'creator', 'video_like_count',
              'video_title', 'upload_timestamp','video_view_count', 'video_id'
              ]
    return df_comments_fans_videos
