import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
df = pd.read_csv('CountryRiskCode.csv')

df['text'] = df['Country'] + '<br>' + \
    df['Code'] + '<br>' + \
    'Main category: '  + df['Category'] + '<br>' + \
    'Category withouth abuse: ' + df['No Abuse'] 

fig = go.Figure(data=go.Choropleth(
    locations = df['Code'],
    z = df['Risk'],
    text = df['text'],
    colorscale = 'Reds',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'number of risk',
))

fig.update_layout(
    title_text='2018 Global Risk',
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

def main():
    fig.show()

main()