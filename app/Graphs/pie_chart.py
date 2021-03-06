import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def active_label(df_user, cutoff_days=None):

  df_user.active_label = df_user.active_label.fillna('other')

  if cutoff_days:
    cutoff_date = pd.datetime.now() - pd.Timedelta(days=cutoff_days)
    df_user = df_user[pd.to_datetime(df_user.timestamp) > cutoff_date]

  pie_data = pd.DataFrame(index=['topFan', 'newFan', 'other', 'trendingFan', 'reEngageFan'])

  pie_data['Fans'] = (df_user
                .groupby('fan_id')
                .active_label
                .first()
                .value_counts(dropna=False)
  )

  pie_data['Comments'] = (df_user
                .active_label
                .value_counts(dropna=False)
  )

  fig = make_subplots(rows=1, cols=2,
                      subplot_titles=("Fans", "Comments"),
                      specs=[[{'type':'domain'}, {'type':'domain'}]])
  fig.add_trace(
      go.Pie(labels=pie_data.index, 
            values=pie_data['Fans'], 
            pull=[0.15, 0, 0, 0, 0], 
            name="Fan %", 
            hole=.4,
            direction ='clockwise',
            sort=False),
    row=1, col=1)

  fig.add_trace(
      go.Pie(labels=pie_data.index, 
            values=pie_data['Comments'],
            marker={'colors': ['#2143AF', 
                                '#6161dc', 
                                '#6f6f6f', 
                                '#196984', 
                                '#193384']},
            pull=[0.15, 0, 0, 0, 0], 
            name="Comment %", 
            hole=.4,
            direction ='clockwise',
            sort=False),
      row=1, col=2)
  
  fig.update_layout(
    title_text="Fan and Comment Distributions")

  return fig