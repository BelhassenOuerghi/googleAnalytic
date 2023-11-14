from datetime import timedelta, datetime
import dash as dash
import dash_mantine_components
from dash import html, dcc, no_update, callback_context
import pandas as pd
from dash.dependencies import Input, Output

from src import sectionTotals, sectionFilters
from src import sectionEvolutionGraphs, sectionReferals
from src import sectionMapGraph
from src.helperFunctions import productsListing, suppliersProductListing, updateOrgDf, updateProdDf
from src.utils import header, footer

#Google Analytics Statistics Assets
df = pd.read_csv(
    './output/bimswarmMarketPlatz-stats.csv',
    index_col='Date',
)
dfReferal = pd.read_csv(
    './output/bimswarmMarketPlatz-stats2.csv',
    index_col='Date',
)
dfProduktStats = pd.read_csv(
    './output/products-stats.csv',
    index_col='Date',
)
dfProduktStatsReferal = pd.read_csv(
    './output/products-stats2.csv',
    index_col='Date',
)

# Statistics Min and Max Date
minDate = df.index.min()
maxDate = df.index.max()

# APP Definition
app = dash.Dash(
    __name__,
    assets_folder='assets/'
)
app.title = 'BIMSWARM-Statistik-Dashboard'
# Application CallBack (Refresh)
@app.callback(
    sectionEvolutionGraphs.output(), sectionTotals.output(), sectionFilters.output(),sectionReferals.output(), sectionMapGraph.output(),Output('products-dropdown','options'),
    [Input("date-picker", "start_date"), Input("date-picker", "end_date"), Input('suppliers-dropdown','value'), Input('products-dropdown','value')]
)
def onChange(startDate, endDate, supplier, product):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

#On Supplier DropDown Choose/Change
    if input_id == "suppliers-dropdown" and supplier != None :
        swarmProductsDB = suppliersProductListing(dfProduktStats, supplier)
        newDf = updateOrgDf(dfProduktStats, supplier)
        newDfReferal = updateOrgDf(dfProduktStatsReferal, supplier)
        return \
                sectionEvolutionGraphs.update(newDf, startDate, endDate)[0],sectionEvolutionGraphs.update(newDf, startDate, endDate)[1], \
                sectionTotals.update(newDf, startDate, endDate)[0], sectionTotals.update(newDf, startDate, endDate)[1], sectionTotals.update(newDf, startDate, endDate)[2],sectionTotals.update(newDf, startDate, endDate)[3],sectionTotals.update(newDf, startDate, endDate)[4], \
                sectionFilters.update(newDf, startDate, endDate)[0],sectionFilters.update(newDf, startDate, endDate)[1], \
                sectionReferals.update(newDfReferal, startDate, endDate)[0],sectionReferals.update(newDfReferal, startDate, endDate)[1], \
                sectionMapGraph.update(newDf, startDate, endDate)[0], \
                swarmProductsDB

#On Product DropDown Empty
    if input_id == "products-dropdown":
        if product == None :
            swarmProductsDB = suppliersProductListing(dfProduktStats, supplier)
            newDf = updateOrgDf(dfProduktStats, supplier)
            newDfReferal = updateOrgDf(dfProduktStatsReferal, supplier)
            return \
                sectionEvolutionGraphs.update(newDf, startDate, endDate)[0],sectionEvolutionGraphs.update(newDf, startDate, endDate)[1], \
                sectionTotals.update(newDf, startDate, endDate)[0], sectionTotals.update(newDf, startDate, endDate)[1], sectionTotals.update(newDf, startDate, endDate)[2],sectionTotals.update(newDf, startDate, endDate)[3],sectionTotals.update(newDf, startDate, endDate)[4], \
                sectionFilters.update(newDf, startDate, endDate)[0],sectionFilters.update(newDf, startDate, endDate)[1], \
                sectionReferals.update(newDfReferal, startDate, endDate)[0],sectionReferals.update(newDfReferal, startDate, endDate)[1], \
                sectionMapGraph.update(newDf, startDate, endDate)[0], \
                swarmProductsDB

#On Product DropDown Choose/Change
        newDf = updateProdDf(dfProduktStats, product)
        newDfReferal = updateProdDf(dfProduktStatsReferal, product)
        return \
            sectionEvolutionGraphs.update(newDf, startDate, endDate)[0],sectionEvolutionGraphs.update(newDf, startDate, endDate)[1], \
                sectionTotals.update(newDf, startDate, endDate)[0], sectionTotals.update(newDf, startDate, endDate)[1], sectionTotals.update(newDf, startDate, endDate)[2],sectionTotals.update(newDf, startDate, endDate)[3],sectionTotals.update(newDf, startDate, endDate)[4], \
                sectionFilters.update(newDf, startDate, endDate)[0],sectionFilters.update(newDf, startDate, endDate)[1], \
                sectionReferals.update(newDfReferal, startDate, endDate)[0],sectionReferals.update(newDfReferal, startDate, endDate)[1], \
                sectionMapGraph.update(newDf, startDate, endDate)[0], \
                no_update

# On Date Picker Change or Supplier DropDown Empty
    return \
    sectionEvolutionGraphs.update(df.loc[endDate:startDate], startDate, endDate)[0],sectionEvolutionGraphs.update(df.loc[endDate:startDate], startDate, endDate)[1], \
    sectionTotals.update(df.loc[endDate:startDate], startDate, endDate)[0], sectionTotals.update(df.loc[endDate:startDate], startDate, endDate)[1], sectionTotals.update(df.loc[endDate:startDate], startDate, endDate)[2],sectionTotals.update(df.loc[endDate:startDate], startDate, endDate)[3],sectionTotals.update(df.loc[endDate:startDate], startDate, endDate)[4],\
    sectionFilters.update(df.loc[endDate:startDate], startDate, endDate)[0],sectionFilters.update(df.loc[endDate:startDate], startDate, endDate)[1],\
    sectionReferals.update(dfReferal.loc[endDate:startDate], startDate, endDate)[0],sectionReferals.update(dfReferal.loc[endDate:startDate], startDate, endDate)[1], \
    sectionMapGraph.update(df.loc[endDate:startDate], startDate, endDate)[0], \
    []


# Analytics Dashboard Layout
app.layout = html.Div(
        [   header(),
            html.Div([
            dcc.Dropdown(options=productsListing(dfProduktStats), placeholder="Anbietern", id='suppliers-dropdown'),
            dcc.Dropdown(options=[], placeholder="Produkte", id='products-dropdown'),
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=minDate,
                max_date_allowed=pd.to_datetime(maxDate) + pd.DateOffset(days=1),
                start_date=datetime.strftime(datetime.strptime((datetime.today() - timedelta(days=30)).isoformat(),'%Y-%m-%dT%H:%M:%S.%f'), '%Y-%m-%d') ,
                end_date=maxDate ,
                display_format="DD/MM/YYYY",
                end_date_id="end-date-el",
                start_date_id="start-date-el"
            ),], className="datepicker-wrapper"),
        sectionTotals.build(df),
        sectionEvolutionGraphs.build(df),
        sectionFilters.build(df),
        sectionReferals.build(dfReferal),
        sectionMapGraph.build(df),
        footer(),
    ],className="container-fluid")

#RUN App on HOST and PORT
if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port=8050)
