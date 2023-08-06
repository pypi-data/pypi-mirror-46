# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dator', 'dator.datastorages', 'dator.transformers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'SQLAlchemy>=1.2.19,<1.3.0',
 'carto>=1.4,<2.0',
 'cartoframes>=0.9.2,<0.10.0',
 'google-cloud-bigquery>=1.11,<2.0',
 'marshmallow>=2.19,<3.0',
 'pandas>=0.24.2,<0.25.0',
 'psycopg2-binary>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'geolibs-dator',
    'version': '0.0.2',
    'description': 'GeoLibs Dator - A data extractor',
    'long_description': "# GeoLibs-Dator\nDator, a data extractor (ETL as a library), that uses Pandas' DataFrames as in memory temporal storage.\n\n### Features\n| Source | Extract | Transform | Load |\n| --- | --- | --- | --- |\n| BigQuery | Y | Y |  |\n| CARTO | Y | Y | Y* |\n| CSV | Y |  | Y |\n| Pandas |  | Y |  |\n| PostgreSQL | Y | Y | Y |\n\n_* Note:_ We are waiting for the append feature on [CARTOframes](https://github.com/CartoDB/cartoframes), because the one we are using is a _ñapa_.\n\n### Configuration\nCreate a `config.yml` file using the `config.example.yml` one as guide. You can find in that one all the possible ETL cases.\n\nIf you are using BigQuery in your ETL process, you need to add a `GOOGLE_APPLICATION_CREDENTIALS` environment variable with the path to your Google Cloud's `credentials.json` file.\n\nYou can test them with the `example.py` file.\n\n### TODOs\n- Better doc.\n- Tests.\n",
    'author': 'Geographica',
    'author_email': 'hello@geographica.com',
    'url': 'https://github.com/GeographicaGS/GeoLibs-Dator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
