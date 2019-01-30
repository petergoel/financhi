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


if __name__ == '__main__':
    unittest.main()
