import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def active_label(df_fans, pie_type='fans'):

  df_fans_labels = df_fans.drop_duplicates(['active_label','fan_id'],keep= 'first')

  num_fans = len(df_fans_labels)
  trend_fans = len(df_fans_labels[df_fans_labels.active_label == 'trendingFan'])
  new_fans = len(df_fans_labels[df_fans_labels.active_label == 'newFan'])
  top_fans = len(df_fans_labels[df_fans_labels.active_label == 'topFan'])
  re_fans = len(df_fans_labels[df_fans_labels.active_label == 'reEngageFan'])
  nan_fans = len(df_fans_labels[df_fans_labels.active_label.isnull()])

  top_fans_com = sum(df_fans.active_label == 'topFan')
  trend_fans_com = sum(df_fans.active_label== 'trendingFan')
  new_fans_com = sum(df_fans.active_label == 'newFan')
  re_fans_com = sum(df_fans.active_label == 'reEngageFan')
  nan_fans_com = sum(df_fans.active_label.isnull())


  labels = ['topFan', 'trendingFan', 'newFan', 'reEngageFan', 'Other']

  # Create subplots: use 'domain' type for Pie subplot
  if pie_type == 'fans':
    fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[top_fans, trend_fans, new_fans, re_fans,nan_fans ], pull=[0.2, 0,0], name="Fan %"),
                1, 1)
    fig.update_layout(title_text="Fan Distribution (Active Badge)")

  elif pie_type == 'comments':
    fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[top_fans_com, trend_fans_com, new_fans_com, re_fans_com, nan_fans_com], pull=[0.2, 0,0], name="Comment %"),
                1, 1)
    fig.update_layout(title_text="Comment Distribution (Active Badge)")
  else:
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[top_fans, trend_fans, new_fans, re_fans,nan_fans ], pull=[0.2, 0,0], name="Fan %"),
                1, 1)
    fig.add_trace(go.Pie(labels=labels, values=[top_fans_com, trend_fans_com, new_fans_com, re_fans_com, nan_fans_com], pull=[0.2, 0,0], name="Comment %"),
                1, 2)
    fig.update_layout(
      title_text="Fan and Comment Distributions (Active Badge)",
      # Add annotations in the center of the donut pies.
      annotations=[dict(text='Fans', x=0.18, y=0.5, font_size=20, showarrow=False),
                  dict(text='Comments', x=0.85, y=0.5, font_size=15, showarrow=False)])

  # Use `hole` to create a donut-like pie chart
  fig.update_traces(hole=.4, hoverinfo="label+percent+name")

  return fig