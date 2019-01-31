# -*- coding: utf-8 -*-
import logging
import os
from .datehelper import *
from .quandlhelper import *
from .plothelper import *
from .financhihelper import *
from .charthelper import *
from .outputhelper import *
from logging.config import fileConfig
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#fileConfig('logging_config.ini')
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)


# Check if path exists
def if_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)