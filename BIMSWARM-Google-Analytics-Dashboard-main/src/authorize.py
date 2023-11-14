from google.analytics.data_v1beta import BetaAnalyticsDataClient, BatchRunReportsRequest, FilterExpressionList
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    MetricType,
    RunReportRequest,
    FilterExpression,
    Filter
)
import pandas as pd

property_id = "332331583"
credentials_json_path = "./bim-swarm-f4cd0c39c284.json"
client = BetaAnalyticsDataClient.from_service_account_json(credentials_json_path)


def getReport(startDate, endDate, products):
    request = BatchRunReportsRequest(
        property =f"properties/{property_id}",
        requests = [RunReportRequest(
            dimensions=[Dimension(name="country"),Dimension(name="date"),Dimension(name="pagePathPlusQueryString"),],
            metrics=[Metric(name='screenPageViews'),Metric(name='sessions'),Metric(name='totalUsers'),Metric(name='userEngagementDuration'),],
            date_ranges=[DateRange(start_date=startDate, end_date=endDate)],
             dimension_filter=FilterExpression(
                 and_group=FilterExpressionList(
                     expressions=[
                         FilterExpression(
                             filter=Filter(
                                 field_name="pagePathPlusQueryString",
                                 string_filter=Filter.StringFilter(
                                     match_type=Filter.StringFilter.MatchType.CONTAINS,
                                     value=products,
                                 ),
                             )
                         )
                     ]
                 )
             )
        )]
    )
    return client.batch_run_reports(request)


def returnReport(response):
    dim = []

    for report in response.reports:
        for rowIdx, row in enumerate(report.rows):
            values = []
            for i, dimension_value in enumerate(row.dimension_values):
                values.append(dimension_value.value)
            for i, metric_value in enumerate(row.metric_values):
                values.append(metric_value.value)
            dim.append(values)
    df = pd.DataFrame(dim, columns=["Land","Date","pagePath","Number of Pages","Sessions","Users","Duration"])
    df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')
    dataf = df.sort_values("Date",  ascending=False)
    return dataf

def getReferalReport(startDate, endDate, products):
    request = BatchRunReportsRequest(
        property =f"properties/{property_id}",
        requests = [RunReportRequest(
            dimensions=[Dimension(name="sessionSource"),Dimension(name="sessionMedium"),Dimension(name="deviceCategory"),Dimension(name="date")],
            metrics=[Metric(name='sessions')],
            date_ranges=[DateRange(start_date=startDate, end_date=endDate)],
             dimension_filter=FilterExpression(
                 and_group=FilterExpressionList(
                     expressions=[
                         FilterExpression(
                             filter=Filter(
                                 field_name="pagePath",
                                 string_filter=Filter.StringFilter(
                                     match_type=Filter.StringFilter.MatchType.CONTAINS,
                                     value=products,
                                 ),
                             )
                         )
                     ]
                 )
             )
        )]
    )
    return client.batch_run_reports(request)


def returnReferalReport(response):
    dim = []
    for report in response.reports:
        for rowIdx, row in enumerate(report.rows):
            values = []
            for i, dimension_value in enumerate(row.dimension_values):
                values.append(dimension_value.value)
            for i, metric_value in enumerate(row.metric_values):
                values.append(metric_value.value)
            dim.append(values)
    df = pd.DataFrame(dim, columns=["Source","Referal","Medium","Date","Sessions",])
    df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')
    dataf = df.sort_values("Date",  ascending=False)
    return dataf


def returnMetricReport(report, StringMetrics):
    dim = []
    val = []
    for rowIdx, row in enumerate(report.rows):
        for i, dimension_value in enumerate(row.dimension_values):
            dimensionHeaders = report.dimension_headers[i].name
            dim.append(dimension_value.value)
        for i, metric_value in enumerate(row.metric_values):
            metricHeaders = report.metric_headers[i].name
            val.append(float(metric_value.value))
    val.reverse()
    dim.reverse()
    df = pd.DataFrame()
    df[StringMetrics] = val
    df = df[[StringMetrics]]
    dataf = df.sort_values(StringMetrics,  ascending=False)
    return dataf



