import json 
import pandas as pd
from datetime import datetime,timedelta
import Process

creds = '/Users/eli/Desktop/creator_profiles_yt/backrest_invoke_prod.json' 
f = open(creds ,) 
credentials_json = json.load(f) 
run_service_url = 'https://backrest-q2zw6yb3ha-uc.a.run.app'
signed_jwt = Process.create_signed_jwt(credentials_json, run_service_url)
token = Process.exchange_jwt_for_token(signed_jwt)

if __name__ == '__main__':
    df = Process.get_full_df(token, 'UCN_fKex8H7MgZiPPzRhgg0A')
    print(df.head())