import plotly
import plotly.graph_objs as go

def show_barchart(df, col):
    res = df.groupby(col)[col].count() #df[col].value_counts()
    data = go.Bar(x=res.index.values, y=res.values)
    plotly.offline.iplot([data])