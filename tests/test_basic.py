# -*- coding: utf-8 -*-
import helper
import logging
import unittest
import datetime as dt

logger = logging.getLogger()


# noinspection SyntaxError,PyUnusedLocal
class BasicTestSuite(unittest.TestCase):

    def test_prev_weekday(self):
        test_date = '2019-01-27'
        prev_weekday_index = 0
        test_date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        expected_date = dt.datetime.strptime('2019-01-25', '%Y-%m-%d').date()
        prev_date = helper.prev_weekday(test_date, prev_weekday_index)

        logger.debug('prev_date is %s & expected date is %s', prev_date,expected_date)

        self.assertEqual(prev_date, expected_date)


if __name__ == '__main__':
    unittest.main()
