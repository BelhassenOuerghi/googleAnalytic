
import pandas as pd
import json
from operator import itemgetter




df = pd.read_csv(
    './output/bimswarmMarketPlatz-stats.csv',
    index_col='Date',
)

