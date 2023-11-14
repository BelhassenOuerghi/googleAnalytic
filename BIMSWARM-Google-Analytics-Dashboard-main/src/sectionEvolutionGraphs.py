from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from src import utils
import plotly.graph_objects as go
from src import htmlComponents


def getFig(df: pd.DataFrame, startDate=None, endDate=None):
    startDate = utils.convertDate(startDate, df, True)
    endDate = utils.convertDate(endDate, df, False)

    dataSessions = df[['Sessions']].astype(float).groupby(df.index).sum()
    dataUsers = df[['Users']].astype(float).groupby(df.index).sum()
    dataDuration = df[['Duration']].astype(float).groupby(df.index).sum()
    dataPages = df[['Number of Pages']].astype(float).groupby(df.index).sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataUsers.index, y=dataUsers['Users'],
                         mode='lines',
                         line={'dash': 'dash', 'color': 'green'},
                         name='Benutzer'))
    fig.add_trace(go.Scatter(x=dataSessions.index, y=dataSessions['Sessions'],
                             mode='lines',
                             line={'dash': 'solid', 'color': 'blue'},
                             name='Sitzungen'))

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=dataDuration.index, y=dataDuration['Duration']/60,
                             mode='lines',
                             line={'dash': 'dash', 'color': 'green'},
                             name='Dauer in Minuten'))
    fig2.add_trace(go.Scatter(x=dataPages.index, y=dataPages['Number of Pages'],
                             mode='lines',
                             line={'dash': 'solid', 'color': 'blue'},
                             name='Anzahl der besuchten Seiten'))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig, fig2


def build(df):
    return html.Div(
        className="row",
        children=[
            htmlComponents.graphCard(
                title="Sitzungen / Benutzer statistiken",
                children=dcc.Graph(
                    id="sessions-evolution-graph",
                    figure={},
                ),
            ),
            htmlComponents.graphCard(
                title="Statistiken zur Dauer/besuchten Seiten",
                children=dcc.Graph(
                    id="transactions-evolution-graph",
                    figure={},
                ),
            ),
        ]
    )


def output():
    return [
        Output(
            component_id="sessions-evolution-graph",
            component_property="figure"
        ),
        Output(
            component_id="transactions-evolution-graph",
            component_property="figure"
        )
    ]


def update(df: pd.DataFrame, startDate, endDate):
    return getFig(df, startDate, endDate)
