import json 
import pandas as pd
from datetime import datetime,timedelta
import Process
import Graphs
import Backrest


raw_data = Backrest.get_raw_data('UCGtHgazkYWXCecFs-OtJc1A')

if __name__ == '__main__':
    df = Process.get_full_df(raw_data)
    #print(df.columns)
    graph = Graphs.get_layout(df)
    print(graph)