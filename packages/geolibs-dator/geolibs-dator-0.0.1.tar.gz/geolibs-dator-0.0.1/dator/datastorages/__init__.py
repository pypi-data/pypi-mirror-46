from datastorages.bigquery import BigQuery
from datastorages.carto import CARTO
from datastorages.csv import CSV
from datastorages.postgresql import PostgreSQL

options = (
    {
        'bigquery': BigQuery,
        'carto': CARTO,
        'csv': CSV,
        'postgresql': PostgreSQL
    }
)
