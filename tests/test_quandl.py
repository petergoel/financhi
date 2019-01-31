# -*- coding: utf-8 -*-
import helper
import logging
import unittest

logger = logging.getLogger(__name__)

class BasicTestSuite(unittest.TestCase):

    def test_get_pivot_data(self):
        symbol = 'CHRIS/CME_ES1'
        start_date = '2019-01-01'
        end_date = '2019-01-29'
        columns = ['High', 'Low', 'Last', 'Settle']

        logger.debug('test_get_pivot_data:: Input Parameters [ %s, %s, %s, %s ]', symbol, start_date, end_date, columns)
        pivot_data = helper.get_pivot_data(symbol, start_date, end_date, columns)
        logger.debug('test_get_pivot_data:: pivot data obtained are %s', pivot_data)
        self.assertEqual(pivot_data.empty, False)

        stock_symbol = 'EOD/SPY'
        logger.debug('test_get_pivot_data:: Input Parameters [ %s, %s, %s, %s ]', stock_symbol, start_date, end_date,
                     columns)
        pivot_data = helper.get_pivot_data(stock_symbol, start_date, end_date)
        logger.debug('test_get_pivot_data:: pivot data obtained are %s', pivot_data)
        self.assertEqual(pivot_data.empty, False)

    def test_get_pivots(self):
        symbol = 'CHRIS/CME_ES1'
        start_date = '2019-01-25'
        end_date = '2019-01-25'
        columns = ['High', 'Low', 'Last', 'Settle']
        settle_column = 'Settle'

        logger.debug('test_get_pivots:: Input Parameters [ %s, %s, %s, %s, %s ]', symbol, start_date,
                     end_date, columns, settle_column)
        pivot_data = helper.get_pivot_data(symbol, start_date, end_date, columns)
        logger.debug('test_get_pivots:: pivot data obtained are %s', pivot_data)
        pivots = helper.get_pivots(pivot_data, settle_column)
        logger.debug('test_get_pivots:: pivots obtained are %s', pivots)

        self.assertEqual(len(pivots), 3)


if __name__ == '__main__':
    unittest.main()
