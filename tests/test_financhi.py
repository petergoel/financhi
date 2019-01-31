# -*- coding: utf-8 -*-
import helper
import logging
import unittest
import pandas as pd
import datetime as dt
import time

logger = logging.getLogger(__name__)
pd.set_option('display.expand_frame_repr', False)

output_dir = '../output/' + dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') + '/'

file_name = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')


class BasicTestSuite(unittest.TestCase):
    def test_get_pivot_data(self):

        # Input Variables
        symbol = 'CHRIS/CME_ES1'
        input_date = '2019-01-30'
        num_days = 10

        # Column variables
        settle_column = 'Settle'
        pivot_column = 'Last'
        columns = ['High', 'Low', 'Last', 'Settle']
        futures_columns = ['Date', 'High', 'Low', 'Last', 'Settle']

        helper.if_exists(output_dir)

        start_date, end_date = helper.get_start_date(input_date, num_days)
        logger.debug('test_get_pivot_data:: [symbol, start date, end date, columns] [ %s, %s, %s, %s ]', symbol,
                     start_date, end_date, columns)

        pivot_df = helper.run_financhi(symbol, start_date, end_date, columns, futures_columns, settle_column,pivot_column)
        (csv_file_name, png_file_name, json_file_name) = helper.generate_file_names(output_dir,symbol,file_name)
        helper.save_output(pivot_df,csv_file_name, png_file_name, json_file_name)
        helper.print_output(pivot_df)


        stock_symbol="EOD/SPY"
        pivot_df = helper.run_financhi(stock_symbol, start_date, end_date)
        (csv_file_name, png_file_name, json_file_name) = helper.generate_file_names(output_dir,stock_symbol,file_name)
        helper.save_output(pivot_df,csv_file_name, png_file_name, json_file_name)
        helper.print_output(pivot_df)

        self.assertEqual(pivot_df.empty, False)


if __name__ == '__main__':
    unittest.main()
