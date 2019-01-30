# -*- coding: utf-8 -*-
from . import datehelper
from . import quandlhelper
from . import plothelper
import numpy as np
import datetime as dt
import ntpath
import time


# TODO Global variables column[], pivotColumn, settleColumn - how to handle?

# Get Symbol Information for plotting in charts
# TODO Streamline logic for columns, pivot and settle
# columns = ['High', 'Low', 'Close'],settleColumn = 'Close',pivotColumn = 'Close' - Equities
# columns = ['High', 'Low', 'Last', 'Settle'],settleColumn = 'Settle',pivotColumn = 'Last' - Futures

def get_symbol_data(symbol, date, pivotColumn='Close', settleColumn='Close', columns=['High', 'Low', 'Close'],
                    noDigits=2, pivot_range=2):
    # Get Date Ranges
    start_date, end_date = datehelper.get_date_ranges(date, pivot_range)

    # Get pivot data
    threeDayPivotData = quandlhelper.get_pivot_data(symbol, start_date, end_date, columns)
    # TODO Returns [] for future dates, add validation
    todayPivotData = quandlhelper.get_pivot_data(symbol, end_date, end_date, columns)

    if (todayPivotData.empty):
        return np.array([np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                         np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                         np.NaN, np.NaN, np.NaN, np.NaN, np.NaN])
    else:
        # Three Day Pivots and Daily Pivots
        threeDayPivots = quandlhelper.get_three_day_pivots(threeDayPivotData, todayPivotData[pivotColumn][0], noDigits)
        dailyPivots = quandlhelper.get_pivots(todayPivotData, settleColumn, noDigits)
        supportResistance = quandlhelper.get_support_resistances(todayPivotData, dailyPivots[0], noDigits)
        return np.array(
            [end_date, symbol, todayPivotData[pivotColumn][0], *threeDayPivots, *dailyPivots, *supportResistance])


# Get Price Data - Returns Date vs. Price for Charting input
def get_price_data(symbol, inputDate, numDays, columns=['High', 'Low', 'Close'], pivotColumn='Close',
                   prev_weekday_index=0):
    inputDate = datehelper.get_prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date(), prev_weekday_index)
    # Get Date Range
    dateList = [inputDate - dt.timedelta(days=x) for x in range(0, int(numDays))]
    holidays = datehelper.get_holidays(dateList[-1], dateList[0])

    priceDataArray = []
    timeDataArray = []

    for date in dateList:
        weekno = date.weekday()
        if weekno < 5:
            print("Getting Data for {}".format(date))
            if dt.datetime.combine(date, dt.datetime.min.time()) in holidays:
                print("Holiday {}".format(date))
            else:
                priceData = quandlhelper.get_pivot_data(symbol, date, date, columns)
                if (priceData.empty):
                    print("Empty Data. Skipping for {}".format(inputDate))
                else:
                    timeDataArray.append(date)
                    priceDataArray.append(priceData[pivotColumn].item())
    return (timeDataArray, priceDataArray)


# Prepare Data - Calls get_symbol_data to get inputs for final chart
# TODO Cleanup code invocation of get_symbol_data
def prepare_data(inputDate, numDays, symbol, prev_weekday_index, noDigits, columns, pivotColumn, settleColumn):
    symbolDataArray = []
    startDate = datehelper.get_prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date(), prev_weekday_index)

    # Get Date Range
    dateList = [startDate - dt.timedelta(days=x) for x in range(0, int(numDays))]
    holidays = datehelper.get_holidays(dateList[-1], dateList[0])

    for date in dateList:
        weekno = date.weekday()
        if weekno < 5:
            print("Getting Data for {}".format(date))
            if dt.datetime.combine(date, dt.datetime.min.time()) in holidays:
                print("Holiday {}".format(date))
            else:
                symbolData = get_symbol_data(symbol, date, noDigits, columns, pivotColumn, settleColumn)
                symbolDataArray.append(symbolData)

    return symbolDataArray


# Prepare Data Plot with 3 day pivots
def prepare_data_plot(inputDate, numDays, symbol, outputDir, fileName):
    startDate = datehelper.get_prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date())
    symbolDataArray = []
    dateArray = []
    priceArray = []
    threeDayPivotArray = []
    threeDayPivotArrayR1 = []
    threeDayPivotArrayR2 = []

    # Constants
    pivotColumn = 'Close'
    settleColumn = 'Close'
    columns = ['High', 'Low', 'Close']
    noDigits = 2

    # Get Date Range
    dateList = [startDate - dt.timedelta(days=x) for x in range(0, int(numDays))]
    holidays = datehelper.get_holidays(dateList[-1], dateList[0])

    for date in dateList:
        weekno = date.weekday()
        if weekno < 5:
            print("Getting Data for {}".format(date))
            if dt.datetime.combine(date, dt.datetime.min.time()) in holidays:
                print("Holiday {}".format(date))
            else:
                symbolData = get_symbol_data(symbol, date, noDigits, pivotColumn, settleColumn, columns)
                symbolDataArray.append(symbolData)
                dateArray.append(symbolData[0])
                priceArray.append(symbolData[2])
                threeDayPivotArray.append(symbolData[3])
                threeDayPivotArrayR1.append(symbolData[4])
                threeDayPivotArrayR2.append(symbolData[5])
    plot_file = outputDir + ntpath.basename(symbol) + "_3day" + dt.datetime.fromtimestamp(time.time()).strftime(
        '%Y-%m-%d-%H-%M-%S') + '.png'
    plothelper.plot_chart_pivots(dateArray, priceArray, threeDayPivotArray, threeDayPivotArrayR1, threeDayPivotArrayR2,
                                 plot_file)
    return
