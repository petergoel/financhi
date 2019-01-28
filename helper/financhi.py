# -*- coding: utf-8 -*-
from . import datehelper
from . import quandlhelper
import numpy as np


# Global variables column[], pivotColumn, settleColumn - how to handle?

# Get Symbol Information
def get_symbol_data(symbol, date, noDigits):
    # Get Date Range
    three_day_pivot_range = 2
    startDate, endDate = datehelper.get_date_ranges(date, three_day_pivot_range)

    # Get pivot data
    threeDayPivotData = quandlhelper.get_pivot_data(symbol, startDate, endDate, columns)
    todayPivotData = quandlhelper.get_pivot_data(symbol, endDate, endDate, columns)

    if (todayPivotData.empty):
        return np.array([np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                         np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                         np.NaN, np.NaN, np.NaN, np.NaN, np.NaN])
    else:
        # Three Day Pivots and Daily Pivots
        threeDayPivots = quandlhelper.get_three_day_pivots(threeDayPivotData, todayPivotData[pivotColumn][0], noDigits)
        dailyPivots = quandlhelper.get_pivots(todayPivotData, noDigits, settleColumn)
        supportResistance = quandlhelper.get_support_resistances(todayPivotData, dailyPivots[0], noDigits)
        return np.array(
            [endDate, symbol, todayPivotData[pivotColumn][0], *threeDayPivots, *dailyPivots, *supportResistance])
