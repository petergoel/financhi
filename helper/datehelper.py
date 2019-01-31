# -*- coding: utf-8 -*-
import numpy as np
import datetime as dt
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import get_calendar, HolidayCalendarFactory, GoodFriday
from datetime import timedelta
import logging

log = logging.getLogger(__name__)

bush_holiday = '2018-12-05'  # George W. Bush Market Holiday


# get holidays
def get_holidays(start_date, end_date):
    # Implement from here https://stackoverflow.com/questions/33094297/create-trading-holiday-calendar-with-pandas/36525605#36525605
    cal = get_calendar('USFederalHolidayCalendar')  # Create calendar instance
    trading_cal = HolidayCalendarFactory('TradingCalendar', cal, GoodFriday)
    # new instance of class
    newcal = trading_cal()
    newcal.rules.pop(7)  # Remove Columbus Day rule
    newcal.rules.pop(7)  # Remove Veteran's Day rule
    holidays = newcal.holidays(start=start_date, end=end_date).to_pydatetime()
    #    holidays = np.append(holidays, dt.datetime.strptime(bush_holiday, '%Y-%m-%d'))
    return holidays


# Get Previous Workday
def get_prev_weekday(input_date, index=0):
    input_date -= timedelta(days=index)
    log.debug("get_prev_weekday:: input date %s", input_date)
    while input_date.weekday() > 4:  # Mon-Fri are 0-4
        input_date -= timedelta(days=1)
    log.debug("get_prev_weekday:: output date %s", input_date)
    return input_date


# Get Date Ranges between two dates
def get_date_ranges(date, pivotRange=2):
    end_date = get_prev_weekday(date)
    start_date = end_date - BDay(pivotRange)
    start_date = start_date.date()
    holidays = get_holidays(start_date, end_date)

    while dt.datetime.combine(start_date, dt.datetime.min.time()) in holidays:
        startDate = get_prev_weekday(start_date, 1)
    log.debug("get_date_ranges:: start date %s", start_date)
    log.debug("get_date_ranges:: end date %s", end_date)
    return (start_date, end_date)


# TODO - Fix logic for Bush Holiday and test holidays in general
# Get Date Ranges between two dates
def get_start_date(date, pivot_range):
    date = dt.datetime.strptime(date, '%Y-%m-%d').date()
    log.debug("get_start_date:: date %s", date)
    end_date = get_prev_weekday(date)
    log.debug("get_start_date:: end_date %s ", end_date)
    start_date = end_date - BDay(int(pivot_range) + 1)
    start_date = start_date.date()

    no_holidays = len(get_holidays(start_date, end_date))
    start_date = get_prev_weekday(start_date, no_holidays)
    log.debug("get_date_ranges:: start date %s", start_date)
    log.debug("get_date_ranges:: end date %s", end_date)
    return (start_date, end_date)
