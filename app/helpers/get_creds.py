import requests
import time
import jwt
import urllib

def create_signed_jwt(credentials_json, run_service_url):
    iat = time.time()
    exp = iat + 3600
    payload = {
        'iss': credentials_json['client_email'],
        'sub': credentials_json['client_email'],
        'target_audience': run_service_url,
        'aud': 'https://www.googleapis.com/oauth2/v4/token',
        'iat': iat,
        'exp': exp
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
    return signed_jwt

def exchange_jwt_for_token(signed_jwt):
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