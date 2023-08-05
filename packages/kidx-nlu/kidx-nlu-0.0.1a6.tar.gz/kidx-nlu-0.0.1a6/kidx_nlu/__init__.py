import logging

import kidx_nlu.version

from kidx_nlu.train import train
from kidx_nlu.test import run_evaluation as test
from kidx_nlu.test import cross_validate
from kidx_nlu.training_data import load_data

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = kidx_nlu.version.__version__
