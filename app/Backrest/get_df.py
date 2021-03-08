import pandas as pd
from app.Backrest.get_data import get_resource

def videos_comment_fans_df(token, platform_account_id):
   
   videos = get_resource(
      resource='/v1/youtube/videos/', 
      params={'creator__youtube_platform_account_id': platform_account_id,
               'limit':1000},
      token=token,
   )

   fans = get_resource(
      resource='/v1/youtube/fans/', 
      params={'creator__youtube_platform_account_id': platform_account_id,
               'limit':1000},
      token=token,
   )

   comments = []
   for video in videos:
      video_id=video['youtube_video_id']
      video_comments = get_resource(
         resource='/v1/youtube/comments/', 
         params={'youtube_video__youtube_platform_video_id':video_id,
                  'limit':1000},
         token=token,
      )
      comments.extend(video_comments)

   df_videos = pd.DataFrame(videos)
   df_fans = pd.DataFrame(fans)
   df_comments = pd.DataFrame(comments)

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
   df_comments_fans_videos.creator = df_comments_fans_videos.creator.str.split('/')
   df_comments_fans_videos.creator = df_comments_fans_videos.creator.str[-2]

   return df_comments_fans_videos
