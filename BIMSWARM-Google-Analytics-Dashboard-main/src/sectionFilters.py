import json
from operator import itemgetter
import plotly.graph_objects as go
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from src import utils


# Génère les graphiques d'évolution grâce à une date de début,
# une date de fin et le dataframe
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

def Update_pagePath(df):

    product = []
    PTG = []
    ptgID, ptgName = ptg()
    df["Sessions"] = df["Sessions"].astype(float)
    for path in enumerate(data):
        for prod in enumerate(path[1]['products']):
            for index, i in df.iterrows():
                splitStr = i['pagePath'].split('&')
                for j in splitStr:
                    if path[1]["URL"] + str(path[1]['products'][prod[1]]) in j:
                        try:
                            value = j.split(path[1]["URL"] + str(path[1]['products'][prod[1]]))
                        except ValueError:
                            print("")
                        else:
                            if value[1] == '' or value[1] == '?tab=0' or value[1] == '?tab=1' or value[1] == '?tab=2':
                                try:
                                    while i['Sessions'] > 0:
                                        product.append(path[1]["Category"] + " / \n" + str(prod[1]))
                                        i['Sessions'] = int(i['Sessions']) - 1
                                    break
                                except ValueError:
                                    print("")


    for iteration in range(len(ptgID)):
        for index, i in df.iterrows():
            splitStr = i['pagePath'].split('&')
            for j in splitStr:
                if 'ptgId=' + str(ptgID[iteration]) in j:
                    try:
                        value = j.split('ptgId=' + str(ptgID[iteration]))
                    except ValueError:
                        print("")
                    else:
                        if value[1] == '' or value[1] == '?tab=0' or value[1] == '?tab=1' or value[1] == '?tab=2':
                            try:
                                while i['Sessions'] > 0:
                                    PTG.append(ptgName[iteration])
                                    i['Sessions'] = int(i['Sessions']) - 1
                                break
                            except ValueError:
                                print("")

    my_dict = {i:PTG.count(i) for i in PTG}
    pathCount = {i: product.count(i) for i in product}
    page = dict(sorted(pathCount.items(), key=itemgetter(1), reverse=True)[:100])
    page2 = dict(sorted(my_dict.items(), key=itemgetter(1), reverse=True)[:100])

    listing = pd.DataFrame.from_dict(page, orient='index', columns=['Number of Visits'])
    listing['Product'] = listing.index
    listing.sort_values(by=['Number of Visits'], ascending=True, inplace=True)

    listing2 = pd.DataFrame.from_dict(page2, orient='index',columns=['Number of Visits'])
    listing2['ProductTyp'] = listing2.index
    listing2.sort_values(by=['Number of Visits'], ascending=True, inplace=True)
    return listing, listing2


def Figure(df, title, title2, ID, graphType,title3):

    height_ = len(df)*40
    if len(df) == 0:
        height_ = 100
    if graphType == 'Bar':
        fig = go.Figure(data=[go.Bar(y=df[title],x=df[title2],orientation='h',text=df[title2],)])
        fig.update_layout(height=height_, margin=dict(t=0, b=0, l=0, r=0),font=dict(family="Arial Black",size=12),)
        return dcc.Graph(className='BarGraph',id=ID,config={"displayModeBar": False},figure=fig), fig
    elif graphType == 'Pie':
        fig = go.Figure(data=[go.Pie(labels=df[title],values=df[title2],direction='clockwise',hole=0.7)])
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0),annotations=[dict(text=title3, x=0.5, y=0.5, font_size=20, showarrow=False)]),
        return dcc.Graph(className='PieChart',id=ID,config={"displayModeBar": False},figure=fig), fig


def build(df):
    return html.Div(
        className="row",
        children=[
            htmlComponents.graphCard(
                title="Verwendete Filter",
                children=dcc.Graph(
                    id="filters-evolution-graph",
                    figure={},
                ),
            ),
            htmlComponents.graphCard(
                title="Verwendete Produkttypfilter",
                children=dcc.Graph(
                    id="typefilters-evolution-graph",
                    figure={},
                ),
            ),
        ]
    )


# Déclare les output à appeler dans le app.callback
def output():
    return [
        Output(
            component_id="filters-evolution-graph",
            component_property="figure"
        ),
        Output(
            component_id="typefilters-evolution-graph",
            component_property="figure"
        ),
    ]


# Fonction qui met à jour les graphiques en fonction de la nouvelle
# date de début et de fin qui lui est donné
def update(df: pd.DataFrame, startDate, endDate):
    listing, listing2 = Update_pagePath(df)
    graph, figure = Figure(listing,'Product', 'Number of Visits', 'PathGraph','Bar',"")
    listing2.sort_values(by=['Number of Visits'], ascending=True, inplace=True)
    graph2, figure2 = Figure(listing2,'ProductTyp', 'Number of Visits', 'ProductTypGraph','Bar',"")
    return figure, figure2
