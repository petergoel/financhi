# -*- coding: utf-8 -*-
from . import datehelper
from . import quandlhelper
import numpy as np
import datetime as dt


# Prepare Data - Calls get_symbol_data to get inputs for final chart
# TODO
def prepare_data(inputDate, numDays, symbol,prev_weekday_index,noDigits,columns,pivotColumn,settleColumn):
    symbolDataArray = []
    startDate = datehelper.prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date(), prev_weekday_index)

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
                symbolData = get_symbol_data(symbol, date, noDigits,columns,pivotColumn,settleColumn)
                symbolDataArray.append(symbolData)

    return symbolDataArray

# TODO Global variables column[], pivotColumn, settleColumn - how to handle?

# Get Symbol Information for plotting in charts
# TODO Streamline logic for columns, pivot and settle
#columns = ['High', 'Low', 'Close'],settleColumn = 'Close',pivotColumn = 'Close' - Equities
#columns = ['High', 'Low', 'Last', 'Settle'],settleColumn = 'Settle',pivotColumn = 'Last' - Futures

def get_symbol_data(symbol, date, noDigits,columns,pivotColumn,settleColumn,pivot_range=2):
    # Get Date Range
    startDate, endDate = datehelper.get_date_ranges(date, pivot_range)

    # Get pivot data
    threeDayPivotData = quandlhelper.get_pivot_data(symbol, startDate, endDate, columns)
    # TODO Returns [] for future dates, add validation
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

# Get Price Data - Returns Date vs. Price for Charting input
# TODO - Externalize pivot column similar to get_symbol_data
def get_price_data(symbol, inputDate, numDays,prev_weekday_index,columns,pivotColumn):
    inputDate = datehelper.prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date(), prev_weekday_index)
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


# Prepare Data Plot with 3 day pivots
def prepare_data_plot(inputDate, numDays, symbol,outputDir,fileName):
    startDate = prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date(), prevweekdayIndex)
    dateArray=[]
    priceArray=[]
    threeDayPivotArray=[]
    threeDayPivotArrayR1=[]
    threeDayPivotArrayR2=[]
    # Get Date Range
    dateList = [startDate - dt.timedelta(days=x) for x in range(0, int(numDays))]
    holidays = get_holidays(dateList[-1], dateList[0])

    for date in dateList:
        weekno = date.weekday()
        if weekno < 5:
            print("Getting Data for {}".format(date))
            if dt.datetime.combine(date, dt.datetime.min.time()) in holidays:
                print("Holiday {}".format(date))
            else:
                symbolData = get_symbol_data(symbol, date, numDigits)
                symbolDataArray.append(symbolData)
                dateArray.append(symbolData[0])
                priceArray.append(symbolData[2])
                threeDayPivotArray.append(symbolData[3])
                threeDayPivotArrayR1.append(symbolData[4])
                threeDayPivotArrayR2.append(symbolData[5])
    plot_file = outputDir + ntpath.basename(symbol) + "_3day"+dt.datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d-%H-%M-%S') + '.png'
    plot_chart_pivots(dateArray,priceArray,threeDayPivotArray,threeDayPivotArrayR1,threeDayPivotArrayR2,plot_file)
    return
