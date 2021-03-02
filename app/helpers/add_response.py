import pandas as pd

def add_received_response_column(df_comments_fans_videos):
  df_responses = df_comments_fans_videos[(df_comments_fans_videos['by_creator'] == True)]
  responded_comments = set(df_responses.parent_comment_id)
  df_comments_fans_videos['received_response'] = df_comments_fans_videos.id.apply(lambda x: x in responded_comments)
  return df_comments_fans_videos