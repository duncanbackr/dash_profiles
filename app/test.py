import json 
import pandas as pd
from datetime import datetime,timedelta
import helpers

creds = '/Users/eli/Desktop/creator_profiles_yt/backrest_invoke_prod.json' 
f = open(creds ,) 
credentials_json = json.load(f) 
run_service_url = 'https://backrest-q2zw6yb3ha-uc.a.run.app'
signed_jwt = helpers.create_signed_jwt(credentials_json, run_service_url)
token = helpers.exchange_jwt_for_token(signed_jwt)


if __name__ == '__main__':
    df = helpers.get_full_df(token, 'UCN_fKex8H7MgZiPPzRhgg0A')
    print(df.head())