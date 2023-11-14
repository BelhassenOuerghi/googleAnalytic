import json
from operator import itemgetter
import plotly.graph_objects as go
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from src import utils
from src import htmlComponents

f = open('Filters.json', 'r', encoding='utf-8')
data = json.load(f)
f = open('ptg.json', 'r', encoding='utf-8')
ptgData = json.load(f)


def ptg():
    ptgID = []
    ptgName = []
    Data = list(ptgData)
    for index in range(len(Data)):
        for key, value in Data[index].items():
            ptgID.append(key)
            ptgName.append(value)

    return ptgID, ptgName


def Update_referals(df, startDate, endDate):
    df['Sessions'] = df['Sessions'].astype(float)

    devicesDf = df[['Sessions', 'Medium']].groupby('Medium')
    devicesDf = devicesDf.sum().reset_index()
    devicesDf = devicesDf.set_index('Medium')

    referalsDf = df[['Sessions', 'Referal']]
    referalsDf['Referal'] = referalsDf['Referal'].replace(['(none)'], 'direct')
    referalsDf = referalsDf.groupby('Referal')
    referalsDf = referalsDf.sum().reset_index()
    referalsDf = referalsDf.set_index('Referal')
    referalsDf.sort_values(by=['Sessions'], ascending=False, inplace=True)
    referalsDf = referalsDf.head(3)

    trafficDf = df[['Sessions', 'Source']]
    trafficDf = trafficDf.groupby('Source')
    trafficDf = trafficDf.sum().reset_index()
    trafficDf = trafficDf.set_index('Source')
    return devicesDf, referalsDf, trafficDf


def Figure(df, title, title2, ID, graphType, title3):


    if graphType == 'Bar':
        fig = go.Figure(data=[go.Bar(x=df.index, y=df[title2], orientation='v', text=df[title2],)])
        fig.update_layout( margin=dict(t=0, b=0, l=0, r=0), font=dict(family="Arial Black", size=12),)
        return dcc.Graph(className='BarGraph', id=ID, config={"displayModeBar": False}, figure=fig), fig
    elif graphType == 'Pie':
        fig = go.Pie(labels=df.index, values=df[title2], direction='clockwise', hole=0.7)
        return "", fig


def build(df):
    return html.Div(
        className="row",
        children=[
            htmlComponents.graphCard(
                title="Sitzungsquelle",
                children=dcc.Graph(
                    id="referal-evolution-graph",
                    figure={},
                ),),
            htmlComponents.graphCard(
                title="Verwendetes Gerät / Empfehlungen",
                children=dcc.Graph(
                    id="devices-evolution-graph",
                    figure={},
                ),), ])


def output():
    return [Output(
            component_id="devices-evolution-graph",
            component_property="figure"),
            Output(
            component_id="referal-evolution-graph",
            component_property="figure"),
    ]


def update(df: pd.DataFrame, startDate, endDate):
    listing, listing2, listing3 = Update_referals(df, startDate, endDate)

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])
    graphDevices, figureDevices = Figure(listing, 'Medium', 'Sessions', 'DevicesGraph', 'Pie', "")
    graphReferal, figureReferals = Figure(listing2, 'Referal', 'Sessions', 'ReferalGraph', 'Pie', "")
    fig.add_trace(figureDevices, row=1, col=1)
    fig.add_trace(figureReferals, row=1, col=2)
    fig.update_traces(hoverinfo="label+percent")
    fig.update_layout(
        annotations=[dict(text='Verwendete Geräte', x=0.10, y=0.5, font_size=15, showarrow=False),
                     dict(text='Sitzungsempfehlungen', x=0.92, y=0.5, font_size=15, showarrow=False)])
    listing3.sort_values(by=['Sessions'], ascending=True, inplace=True)

    graph2, figure2 = Figure(listing3, 'Source', 'Sessions', 'SourcesGraph','Bar',"")

    return [fig, figure2]
