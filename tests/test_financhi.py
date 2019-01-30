# -*- coding: utf-8 -*-
import helper
import logging
import unittest
import datetime as dt

logger = logging.getLogger()


class BasicTestSuite(unittest.TestCase):

    def test_get_symbol_data(self):
        symbol = 'EOD/SPY'
        input_date = '2019-01-24'
        input_date = dt.datetime.strptime(input_date, '%Y-%m-%d').date()
        # Futures parameters
        columns = ['High', 'Low', 'Last', 'Settle']
        pivot_column = 'Last'
        settle_column = 'Settle'
        num_digits = 2

        symbol_data = helper.get_symbol_data(symbol, input_date)
        logger.debug('symbol data obtained  for %s is %s', symbol, symbol_data)
        self.assertEqual(len(symbol_data), 15)

        futures_symbol = 'CHRIS/CME_ES1'
        symbol_data = helper.get_symbol_data(futures_symbol, input_date, pivot_column, settle_column, columns)
        logger.debug('symbol data obtained for %s  is %s', futures_symbol, symbol_data)
        self.assertEqual(len(symbol_data), 15)

    def test_get_price_data(self):
        symbol = 'EOD/SPY'
        input_date = '2019-01-24'
        num_days = 10

        # Futures parameters
        columns = ['High', 'Low', 'Last', 'Settle']
        pivot_column = 'Last'

        time_array, price_array = helper.get_price_data(symbol, input_date, num_days)
        logger.debug('[time_array,price_array] obtained is %s, %s', time_array, price_array)
        self.assertEqual(len(time_array), 7)
        self.assertEqual(len(price_array), 7)

        futures_symbol = 'CHRIS/CME_ES1'
        time_array, price_array = helper.get_price_data(futures_symbol, input_date, num_days, columns, pivot_column)
        logger.debug('[time_array,price_array] obtained is %s, %s', time_array, price_array)
        self.assertEqual(len(time_array), 7)
        self.assertEqual(len(price_array), 7)

    def test_prepare_data(self):
        symbol = 'EOD/SPY'
        input_date = '2019-01-24'
        num_days = 10
        # Futures parameters
        columns = ['High', 'Low', 'Last', 'Settle']
        pivot_column = 'Last'
        settle_column = 'Settle'

        symbol_data_array = helper.prepare_data(input_date, num_days, symbol)
        logger.debug('symbol data array obtained  for %s is %s', symbol, symbol_data_array)
        self.assertEqual(len(symbol_data_array), 7)

        futures_symbol = 'CHRIS/CME_ES1'
        symbol_data_array = helper.prepare_data(input_date, num_days, futures_symbol, pivot_column, settle_column,
                                                columns)
        logger.debug('symbol data array obtained for %s  is %s', futures_symbol, symbol_data_array)
        self.assertEqual(len(symbol_data_array), 7)


if __name__ == '__main__':
    unittest.main()
