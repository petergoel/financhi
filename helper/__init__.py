# -*- coding: utf-8 -*-
import logging
import os
from .datehelper import *
from logging.config import fileConfig

fileConfig('logging_config.ini')

# Check if path exists
def if_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)
