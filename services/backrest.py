from typing import Dict
import sys
import requests
import datetime

from app import config

def get_headers(target_service):
    metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='

    token_request_url = metadata_server_token_url + target_service
    token_request_headers = {'Metadata-Flavor': 'Google'}

    # Fetch the token
    token_response = requests.get(token_request_url, headers=token_request_headers)
    jwt = token_response.content.decode("utf-8")

    # Provide the token in the request to the receiving service
    return {'Authorization': f'bearer {jwt}'}


def get_creator(creator_id=None,
                channel_id=None,
                backrest_url=config.BACKREST_URL) \
        -> requests.Response:
    """
    Requests creator details from Backrest

    params: 
        creator_id: int,
    returns:
        ResponseObject(
            {
                "url": str,
                "channel_id": str,
                "channel_name": str,
                "thumbnail": str
            },
            200)
    """
    backrest_headers = get_headers(backrest_url.geturl())
    #backrest_headers = None
    if creator_id:
        return requests.get(f"{backrest_url.geturl()}youtube/creators/{creator_id}/", headers=backrest_headers)
    else:
        return requests.get(f"{backrest_url.geturl()}youtube/creators/", 
                            params={'youtube_platform_account_id':channel_id},
                            headers=backrest_headers)



def get_videos_list(
                    channel_id: str,
                    num_vids=None,
                    backrest_url=config.BACKREST_URL) \
    -> requests.Response:
    """
    Request all videos from backrest for a given channel

    params:
        channel_id: str,
        num_vids: int,
    returns:
        ResponseObject(
            {
                "count": 8,
                "next": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/videos/?channel_id=UCtHoTrH0GgJ9fBrzmTqk7Pg&limit=2&offset=2",
                "previous": null,
                "results": [
                    {
                        "url": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/videos/641/",
                        "creator": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/creators/59/",
                        "likes": 9070,
                        "thumbnail": "https://i.ytimg.com/vi/TUrN7tuB8Xw/sddefault.jpg",
                        "title": "CARYS - When A Girl (Official Music Video)",
                        "uploaded": "2020-10-02T04:00:04Z",
                        "views": 497288,
                        "youtube_video_id": "TUrN7tuB8Xw"
                    },
                    {
                        "url": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/videos/642/",
                        "creator": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/creators/59/",
                        "likes": 1498,
                        "thumbnail": "https://i.ytimg.com/vi/ABOnzgV2PeE/sddefault.jpg",
                        "title": "CARYS - Crush (visualizer)",
                        "uploaded": "2020-08-28T04:00:01Z",
                        "views": 62450,
                        "youtube_video_id": "ABOnzgV2PeE"
                    }
                ]
            },
            200)
    """
    backrest_headers = get_headers(backrest_url.geturl())
    return requests.get(f"{backrest_url.geturl()}youtube/videos/",
                    params={'creator__youtube_platform_account_id':channel_id},
                    headers=backrest_headers)

def get_fans_list(
                    channel_id: int,
                    limit = 1000,
                    backrest_url=config.BACKREST_URL) \
    -> requests.Response:
    """
    Get list of all fans from backrest

    params:
        channel_id: str,
        limit: int
    returns:
        ResponseObject(
        {
            "count": 9029,
            "next": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/fans/?channel_id=UCtHoTrH0GgJ9fBrzmTqk7Pg&limit=2&offset=2",
            "previous": null,
            "results": [
                {
                    "url": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/fans/90956/",
                    "youtube_channel_id": "UCiUF3O3zAyKmWbbvdzBAm4w",
                    "youtube_channel_name": "_",
                    "thumbnail": "https://yt3.ggpht.com/ytc/AAUvwnidhdm1TZ1hr4kXrLq0WaGzfW8nvrSlJlzqBg-Fug=s48-c-k-c0xffffffff-no-rj-mo",
                    "note": null,
                    "creator": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/creators/59/",
                    "shopify_customer": null
                },
                {
                    "url": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/fans/92252/",
                    "youtube_channel_id": "UCj06yULephm__ipwIJDqZRA",
                    "youtube_channel_name": "_우주¿¡",
                    "thumbnail": "https://yt3.ggpht.com/ytc/AAUvwnjndY_rsM1R6z_YQOcM9Ybd4hd5CEcfrLQSr8Hf=s48-c-k-c0xffffffff-no-rj-mo",
                    "note": null,
                    "creator": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/creators/59/",
                    "shopify_customer": null
                }
            ]
        },
        200)
    """
    backrest_headers = get_headers(backrest_url.geturl())
    return requests.get(f"{backrest_url.geturl()}youtube/fans/",
                        params={
                            'creator__youtube_platform_account_id':channel_id,
                            'limit':limit
                            },
                        headers=backrest_headers)

def get_next_page(url, backrest_url=config.BACKREST_URL):
    """ Gets next page of a request """
    
    backrest_headers = get_headers(backrest_url.geturl())
    #backrest_headers = None
    return requests.get(url, headers=backrest_headers)

def get_video_comments(
                    video_id: str,
                    limit=1000,
                    backrest_url=config.BACKREST_URL) \
    -> requests.Response:
    """
    Gets latest comment or reply for a video
    params:
        video_id: str,
        reply: bool,
    returns:
        ResponseObject(
            {
            "count": 213885,
            "next": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/comments/?format=json&limit=1&offset=1&ordering=%5B-upload_timestamp%5D&video=3DcGQZGMM4Tf8",
            "previous": null,
            "results": [
                {
                    "url": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/comments/62906/?format=json",
                    "archived": false,
                    "backr_reply": false,
                    "by_creator": false,
                    "content": "This shit is classic",
                    "created": "2012-12-30T18:06:06Z",
                    "downvote": null,
                    "fan": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/fans/44341/?format=json",
                    "likes": 0,
                    "upvote": null,
                    "video": "https://backrest-ydzki5e7sq-uc.a.run.app/v1/youtube/videos/475/?format=json",
                    "youtube_comment_id": "UgxONq5VmE4q787v6rB4AaABAg"
                    }
                ]
            },
            200)
    """
    backrest_headers = get_headers(backrest_url.geturl())
    #backrest_headers = None
    return requests.get(f"{backrest_url.geturl()}youtube/comments/",
                        params={'youtube_video__youtube_platform_video_id':video_id,
                                'limit':limit},
                        headers=backrest_headers)
