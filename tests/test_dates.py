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
        test_date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        expected_date = dt.datetime.strptime('2019-01-25', '%Y-%m-%d').date()
        prev_date = helper.get_prev_weekday(test_date)

        logger.debug('prev_date is %s & expected date is %s', prev_date, expected_date)

        self.assertEqual(prev_date, expected_date)

    def test_get_holidays(self):
        start_date = '2018-01-01'
        end_date = '2019-01-01'

        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
        holiday_list = helper.get_holidays(start_date, end_date)

        logger.debug("Holidays in 2018 is %s", holiday_list)
        self.assertIsNotNone(holiday_list)

    def test_get_date_ranges(self):
        input_date = '2019-01-29'
        test_date = '2019-01-25'
        input_date = dt.datetime.strptime(input_date, '%Y-%m-%d').date()
        start_date, end_date = helper.get_date_ranges(input_date)

        logger.debug("start date and end date for  %s are: %s %s", input_date, start_date, end_date)
        self.assertEqual(end_date, input_date)
        self.assertEqual(start_date, dt.datetime.strptime(test_date, '%Y-%m-%d').date())


if __name__ == '__main__':
    unittest.main()
