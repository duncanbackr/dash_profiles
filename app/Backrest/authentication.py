import requests
from config import Config
import time
import json
import jwt
import urllib

def get_token(target_service):

    if Config.LOCAL:

        f = open(Config.CREDENTIALS_PATH) 
        credentials_json = json.load(f) 

        payload = {
            'iss': credentials_json['client_email'],
            'sub': credentials_json['client_email'],
            'target_audience': target_service,
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'iat': time.time(),
            'exp': time.time() + 3600
            }
        additional_headers = {
            'kid': credentials_json['private_key_id']
            }
        signed_jwt = jwt.encode(
            payload, 
            credentials_json['private_key'], 
            headers=additional_headers,
            algorithm='RS256'
            )
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': signed_jwt
        }
        token_request = requests.post(
            url = 'https://www.googleapis.com/oauth2/v4/token',
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data = urllib.parse.urlencode(body)
        )
        return token_request.json()['id_token']

    metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='

    token_request_url = metadata_server_token_url + target_service
    token_request_headers = {'Metadata-Flavor': 'Google'}

    # Fetch the token
    token_response = requests.get(token_request_url, headers=token_request_headers)
    token = token_response.content.decode("utf-8")

    # Provide the token in the request to the receiving service
    return token