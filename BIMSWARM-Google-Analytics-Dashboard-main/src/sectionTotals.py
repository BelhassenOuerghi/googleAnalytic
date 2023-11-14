from dash import html
import pandas as pd
from dash.dependencies import Input, Output
from src import utils
from src import htmlComponents


def getTotals(df: pd.DataFrame, startDate=None, endDate=None):
    startDate = utils.convertDate(startDate, df, True)
    endDate = utils.convertDate(endDate, df, False)
    totalUsers = df['Users'].astype(float).sum()
    totalSessions = df['Sessions'].astype(float).sum()
    totalDuration = df['Duration'].astype(float).sum()
    avgNumberPages = round(df['Number of Pages'].astype(float).sum()/totalUsers, 2)
    avgDuration = totalDuration / totalSessions
    return totalUsers, totalSessions, convert_to_preferred_format(totalDuration), avgNumberPages, convert_to_preferred_format(avgDuration)


def convert_to_preferred_format(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minute = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, minute, sec)


def build(df: pd.DataFrame):
    totals = getTotals(df)
    content = htmlComponents.totalCardsWrapper([
        htmlComponents.totalCard(
            label="Gesamtzahl der Benutzer",
            value=totals[0],
            id="total-users"
        ),
        htmlComponents.totalCard(
            label="Gesamtzahl der Sitzungen",
            value=totals[1],
            id="total-sessions"
        ),
        htmlComponents.totalCard(
            label="Gesamtdauer",
            value=totals[2],
            id="total-transactions"
        ),
        htmlComponents.totalCard(
            label="Durchschnittliche Anzahl der pro Benutzer besuchten Seiten",
            value=totals[3],
            id="total-revenues"
        ),
        htmlComponents.totalCard(
            label="Durchschnittliche Dauer pro Sitzung",
            value=totals[4],
            id="total-conversion"
        ),
    ])
    return html.Div([content], className="row")


def output():
    return [
        Output(
            component_id="total-users",
            component_property="children"
        ),
        Output(
            component_id="total-sessions",
            component_property="children"
        ),
        Output(
            component_id="total-transactions",
            component_property="children"
        ),
        Output(
            component_id="total-revenues",
            component_property="children"
        ),
        Output(
            component_id="total-conversion",
            component_property="children"
        ),
    ]


def update(df: pd.DataFrame, startDate, endDate):
    return getTotals(df, startDate, endDate)