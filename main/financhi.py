# -*- coding: utf-8 -*-
import helper
import logging
import pandas as pd
import ntpath
import datetime as dt
import time
import os
import sys, getopt

logger = logging.getLogger(__name__)
pd.set_option('display.expand_frame_repr', False)


def if_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

# Main function
def main(argv):
    # Default values
    symbol = 'CHRIS/CME_ES1'
    input_date = '2019-01-30'
    num_days = 10
    symbol_type = 'F'
    output_dir = '../output/' + dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') + '/'
    #output_dir = ''
    file_name = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

    # Column variables
    settle_column = 'Settle'
    pivot_column = 'Last'
    columns = ['High', 'Low', 'Last', 'Settle']
    futures_columns = ['Date', 'High', 'Low', 'Last', 'Settle']
    if_exists(output_dir)

    try:
        opts, args = getopt.getopt(argv, "hs:d:n:t:", ["symbol=", "date=", "days=", "type="])
    except getopt.GetoptError:
        print('financhi.py -s <symbol> -d<date> -n <days> -t <type>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('financhi.py -s <symbol> -d<date> -n <days> -t <type>')
            sys.exit()
        elif opt in ("-s", "--symbol"):
            symbol = arg
        elif opt in ("-d", "--date"):
            input_date = arg
        elif opt in ("-n", "--days"):
            num_days = arg
        elif opt in ("-t", "--type"):
            symbol_type = arg
        else:
            print("No arguments....")
            sys.exit(2)

    (start_date, end_date) = helper.get_start_date(input_date, num_days)
    logger.debug('main:: [symbol, start date, end date, num days, type] [ %s, %s, %s %s %s ]', symbol, start_date,
                 end_date, num_days, symbol_type)

    if symbol_type.upper() == 'F':
        pivot_df = helper.run_financhi(symbol, start_date, end_date, columns, futures_columns, settle_column,
                                       pivot_column)

    else:
        pivot_df = helper.run_financhi(symbol, start_date, end_date)

    (csv_file_name, png_file_name, json_file_name) = helper.generate_file_names(output_dir, symbol, file_name)
    logger.debug('main:: [csv_file_name, png_file_name date, json_file_name ] [ %s, %s, %s  ]', csv_file_name, png_file_name, json_file_name)

    helper.save_output(pivot_df, csv_file_name, png_file_name, json_file_name)
    helper.print_output(pivot_df)

if __name__ == "__main__":
    main(sys.argv[1:])
