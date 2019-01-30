# -*- coding: utf-8 -*-
import numpy as np
import datetime as dt
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import get_calendar, HolidayCalendarFactory, GoodFriday
from datetime import timedelta
import logging

log = logging.getLogger(__name__)

bush_holiday = '2018-12-05'  # George W. Bush Market Holiday
prev_week_day_index = 0


# get holidays
def get_holidays(startDate, endDate):
    # Implement from here https://stackoverflow.com/questions/33094297/create-trading-holiday-calendar-with-pandas/36525605#36525605
    cal = get_calendar('USFederalHolidayCalendar')  # Create calendar instance
    tradingCal = HolidayCalendarFactory('TradingCalendar', cal, GoodFriday)
    # new instance of class
    newcal = tradingCal()
    newcal.rules.pop(7)  # Remove Columbus Day rule
    newcal.rules.pop(7)  # Remove Veteran's Day rule
    holidays = newcal.holidays(start=startDate, end=endDate).to_pydatetime()
    holidays = np.append(holidays, dt.datetime.strptime(bush_holiday, '%Y-%m-%d'))
    return holidays


# Get Previous Workday
def get_prev_weekday(adate, index=0):
    adate -= timedelta(days=index)
    log.debug("input date", adate)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    log.debug("output date", adate)
    return adate


# Get Date Ranges between two dates
def get_date_ranges(date, pivotRange=2):
    endDate = get_prev_weekday(date)
    startDate = endDate - BDay(pivotRange)
    startDate = startDate.date()
    holidays = get_holidays(startDate, endDate)

    while dt.datetime.combine(startDate, dt.datetime.min.time()) in holidays:
        startDate = get_prev_weekday(startDate, 1)
    return (startDate, endDate)
