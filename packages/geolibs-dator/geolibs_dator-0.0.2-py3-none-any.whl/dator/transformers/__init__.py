from transformers.bigquery import BigQuery
from transformers.pandas import Pandas
from transformers.postgresql import PostgreSQL

options = (
    {
        'bigquery': BigQuery,
        'carto': PostgreSQL,
        'pandas': Pandas,
        'postgresql': PostgreSQL
    }
)
