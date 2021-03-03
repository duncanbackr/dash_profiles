import pandas as pd
import numpy as np

def get_cutoff(df_fan_metrics):
    mean_num_comments = np.mean(df_fan_metrics['total_comments'])
    std_comments = np.std(df_fan_metrics['total_comments'])

    top_fan_cutoff = mean_num_comments + 2*std_comments

    return top_fan_cutoff
