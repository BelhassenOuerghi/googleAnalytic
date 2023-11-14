import json
from urllib.request import urlopen
import geopandas
import numpy as np
import plotly.express as px
from dash import html, dcc
import pandas as pd
import dash.dependencies as dd
import plotly.validator_cache
import plotly.graph_objects
from src import htmlComponents
import requests





worldmap = requests.get(
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
).json()

def getFig(df: pd.DataFrame, startDate, endDate):
    # Renomme les régions pour rendre compatible avec celles de Google Analytics
    renameRegionNames(worldmap)
    df['Sessions'] =df['Sessions'].astype(float)
    dataSessions = df[['Sessions','Land']].groupby('Land').sum()
    dataSessions['Sessions'] = dataSessions['Sessions'].fillna(0.0)
    dataSessions = dataSessions.drop_duplicates()


    figmap = px.choropleth(
    dataSessions,
    locations=dataSessions.index,
    color="Sessions",
    color_continuous_scale="Algae",
    range_color=[20, 10],
)

    figmap = px.choropleth_mapbox(
    dataSessions,
    locations=dataSessions.index,
    geojson=worldmap,
    featureidkey="properties.NAME",
    color="Sessions",
    color_continuous_scale="Algae",
    range_color=[20, 10],
    mapbox_style="carto-positron",
    zoom=4,
    center={
            "lat": 49.71109,
            "lon": 0.5},
    height=600,
    opacity=0.75,
    labels={
            'Sessions': 'Sitzungen',
            'City': 'Stadt'}
    ).update_layout(mapbox={"zoom": 2})

    return figmap


# Génère le html pour la map et le selector
def build(df):
    return html.Div(
        className="row",
        children=htmlComponents.mapCard(
            title="Geografische Anzahl der Besuche",
            dropDown=dcc.Dropdown(
                disabled=True,
                id= 'map-dropdown'
            ),
            map=dcc.Graph(
                id='transactions-per-region-map',
                figure={}
            )
        )
    )


def renameRegionNames(geoJSON: dict):
    for item in geoJSON['features']:
        item['properties']['NAME'] = renameRegionName(item['properties']['NAME'])


def renameRegionName(regionName: str):
    overrideNames = {
        "United States of America": "United States",
        "Fr. S. Antarctic Lands": "France",

    }

    if (regionName in overrideNames.keys()):
        regionName = overrideNames[regionName]
    return regionName


# Recupère les noms des régions depuis le geoJSON
def getRegionsNames(geoJSON: dict):
    renameRegionNames(geoJSON)
    output = []
    for item in geoJSON['features']:
        output.append( item['properties']['NAME'])
    return output


# Génère la liste de régions pour la dropdown
def buildDropdownOptions(geoJSON: dict):
    output = []
    for item in geoJSON['features']:
        output.append({
            'label': item['properties']['NAME'],
            'value': renameRegionName(item['properties']['NAME'],)
        })
    return sorted(output, key=lambda el: el['label'])


def output():
    return [dd.Output(
        component_id="transactions-per-region-map",
        component_property="figure"
    )]


def update(df: pd.DataFrame, startDate, endDate):
    return [getFig(df, startDate, endDate)]
