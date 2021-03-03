import pandas as pd
def fan_type(x,top_fan_cutoff):
    if x == 1:
        return 'NewFan'
    elif (x > 1) & (x < top_fan_cutoff):
        return 'TrendFan'
    else:
        return 'TopFan' 

def add_label(df_user, top_fan_cutoff):
        
    if top_fan_cutoff < 3:
        top_fan_cutoff = 3

    df_user['passive_label']  =  df_user.cum_count.apply(lambda x: fan_type(x, top_fan_cutoff))
    return df_user
