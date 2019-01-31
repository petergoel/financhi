# -*- coding: utf-8 -*-
import logging
from .datehelper import get_start_date
from .financhihelper import run_financhi
from .outputhelper import if_exists
from .outputhelper import generate_file_names
from .outputhelper import save_output
from .outputhelper import print_output
from logging.config import fileConfig
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# fileConfig('logging_config.ini')
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)



