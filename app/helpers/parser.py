import pandas as pd
from datetime import datetime,timedelta
def parse_timestamp(df):
    df['dates'] = [d.date() for d in df['timestamp']]
    df['times'] = [d.time() for d in df['timestamp']]

    df['times'] = pd.to_datetime(df.times, format='%H:%M:%S')
    df['dates'] = pd.to_datetime(df.dates, format='%Y-%m-%d')

    df['month'] = df['dates'].dt.strftime('%m')

    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    df = df.replace({"month": months})

    df['year'] = df['dates'].dt.strftime('%Y')

    df['day'] = df['dates'].apply(lambda time: time.dayofweek)

    days = {0: "Mon", 1: "Tues", 2: "Wed", 3: "Thurs", 4: "Fri", 5: "Sat", 6: "Sun"}
    df = df.replace({"day": days})

    df['hours'] = df['times'].dt.strftime('%H')

    return df