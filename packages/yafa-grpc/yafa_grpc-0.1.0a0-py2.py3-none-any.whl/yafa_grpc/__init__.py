__author__ = 'Graham Crowell'
__email__ = 'graham.crowell@gmail.com'
__version__ = '0.1.0alpha'

import os

DATA_WAREHOUSE_HOST = os.getenv("DATA_WAREHOUSE_HOST")
assert DATA_WAREHOUSE_HOST, "missing required environment variable: DATA_WAREHOUSE_HOST"

import logging

LOGGING_VERBOSITY = logging.DEBUG
