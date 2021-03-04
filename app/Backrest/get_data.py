import requests

def get_videos(token, platform_account_id):
    videos = []
    results = requests.get(
        url = 'https://backrest-q2zw6yb3ha-uc.a.run.app/v1/youtube/videos/', 
        params = {'creator__youtube_platform_account_id': platform_account_id,
                  'limit':100},
                  headers = {
                      'Authorization': f'Bearer {token}'})
    videos.extend(results.json()['results'])
    next = results.json()['next']
    while next:
        results = requests.get(
            url = next,
            headers = {
                'Authorization': f'Bearer {token}'
            }
        )
        videos.extend(results.json()['results'])
        next = results.json()['next']
    return videos

def get_comments(token, platform_account_id):
    videos = get_videos(token, platform_account_id)
    comments = []
    # i=0
    for video in videos:
        video_id=video['youtube_video_id']

        results = requests.get(
            url = 'https://backrest-q2zw6yb3ha-uc.a.run.app/v1/youtube/comments/',
            params = {
                'youtube_video__youtube_platform_video_id':video_id,
                'limit':10000},
            headers = {
                'Authorization': f'Bearer {token}'
            }
        )
        comments.extend(results.json()['results'])

        next = results.json()['next']
        while next:
            results = requests.get(
            url = next,
            headers = {
                'Authorization': f'Bearer {token}'
            }
            )
            comments.extend(results.json()['results'])
            next = results.json()['next']
    return comments


def get_fans(token, platform_account_id):

    results2 = requests.get(
        url = 'https://backrest-q2zw6yb3ha-uc.a.run.app/v1/youtube/fans/',
        params = {
            'creator__youtube_platform_account_id': platform_account_id,
            'limit':10000},
        headers = {
            'Authorization': f'Bearer {token}'
        }
    )
    fans = results2.json()['results']
    next = results2.json()['next']
    while next:
        results2 = requests.get(
            url = next,
            headers = {
                'Authorization': f'Bearer {token}'
            }
        )
        fans.extend(results2.json()['results'])
        next = results2.json()['next']
    return fans 

def get_creators(token):
    results_creator = requests.get(
    url = "https://backrest-q2zw6yb3ha-uc.a.run.app/v1/youtube/creators/",

    headers = {
        'Authorization': f'Bearer {token}'
        }   
    )
    creator = results_creator.json()
    return creator
