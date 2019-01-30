# -*- coding: utf-8 -*-
import logging
import os
from .datehelper import *
from .quandlhelper import *
from .plothelper import *
from .financhi import *
from logging.config import fileConfig

fileConfig('logging_config.ini')

# Check if path exists
def if_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


class Stock:

    def __init__(self,date,price,high,low,close):

class Futures:
        def __init__(self, date, price, high, low, close):