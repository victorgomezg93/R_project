import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('CountryRiskCode.csv')


fig = go.Figure(data=go.Choropleth(
    locations = df['Code'],
    z = df['Risk'],
    text = df['Code'],
    colorscale = 'Reds',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'number of risk',
))

fig.update_layout(
    title_text='Global Risk',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: Data Driven Class',
        showarrow = False
    )]
)



fig.show()


