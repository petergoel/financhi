# -*- coding: utf-8 -*-
import helper
import logging
import unittest

logger = logging.getLogger()


class BasicTestSuite(unittest.TestCase):

    def test_get_pivot_data(self):
        symbol = 'CHRIS/CME_ES1'
        start_date = '2019-01-25'
        end_date = '2019-01-26'
        columns = ['High', 'Low', 'Last', 'Settle']

        pivot_data = helper.get_pivot_data(symbol, start_date, end_date,columns)
        logger.debug('pivot data obtained is %s', pivot_data)
        self.assertEqual(pivot_data.empty,False)

        stock_symbol = 'EOD/SPY'
        pivot_data = helper.get_pivot_data(stock_symbol, start_date, end_date)
        logger.debug('pivot data obtained is %s', pivot_data)
        self.assertEqual(pivot_data.empty, False)

    def test_get_pivots(self):
        symbol = 'CHRIS/CME_ES1'
        start_date = '2019-01-23'
        end_date = '2019-01-23'
        columns = ['High', 'Low', 'Last', 'Settle']
        settle_column = 'Settle'

        pivot_data = helper.get_pivot_data(symbol, end_date, end_date,columns)
        pivots=helper.get_pivots(pivot_data,settle_column)
        logger.debug('pivots obtained is %s', pivots)
        self.assertEqual(len(pivots),3)

        stock_symbol='EOD/SPY'
        pivot_data = helper.get_pivot_data(stock_symbol, end_date, end_date)
        pivots = helper.get_pivots(pivot_data)
        logger.debug('pivots obtained is %s', pivots)
        self.assertEqual(len(pivots), 3)

    def test_get_three_day_pivots(self):
        symbol = 'CHRIS/CME_ES1'
        start_date = '2019-01-23'
        end_date = '2019-01-25'
        columns = ['High', 'Low', 'Last', 'Settle']
        settle_column = 'Settle'

        pivot_data = helper.get_pivot_data(symbol, start_date, end_date,columns)
        settle=pivot_data[settle_column][0]
        pivots=helper.get_pivots(pivot_data,settle_column)
        logger.debug('pivots obtained is %s', pivots)
        three_day_pivots = helper.get_three_day_pivots(pivot_data, settle)
        logger.debug('three day pivots obtained is %s', three_day_pivots)
        self.assertEqual(len(three_day_pivots),3)

if __name__ == '__main__':
    unittest.main()
