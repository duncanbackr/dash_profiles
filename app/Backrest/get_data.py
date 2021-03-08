import requests
from config import Config

def get_resource(resource:str,
                 params:dict,
                 token:str,
                 backrest_url=Config.BACKREST_URL):

    data = []
    results = requests.get(
        url = backrest_url + resource, 
        params = params,
        headers = {
            'Authorization': f'Bearer {token}'}
        )

    if type(results.json()) is list:
        return results.json()

    data.extend(results.json()['results'])
    next = results.json()['next']
    while next:
        results = requests.get(
            url = next,
            headers = {
                'Authorization': f'Bearer {token}'
            }
        )

        # TODO add an error catch

        data.extend(results.json()['results'])
        next = results.json()['next']
    return data

