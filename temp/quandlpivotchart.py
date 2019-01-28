import quandl
import numpy as np
import datetime as dt
import pandas as pd
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.holiday import get_calendar, HolidayCalendarFactory, GoodFriday
from datetime import timedelta
import sys, getopt
import time
import os
import matplotlib
# matplotlib.use('agg')
from matplotlib import pyplot, dates
import ntpath
import boto3
import logging

#Pandas init option
pd.set_option('display.expand_frame_repr', False)

#Logging for AWS
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.ERROR)

#Variables for AWS to copy to S3 bucket
bucket_name = "quandl-stock-charts"
lambda_path = "/tmp/"

# API Key
# quandl.read_key()
quandl.ApiConfig.api_key = 'myUW3XaM4eC7WEzTXzZA'
# Constants
chartDays = 10
numDays = 1
numDigits = 2

# George W Bush Holiday
bushHoliday = '2018-12-05'

# Global Variables
columns = ['High', 'Low', 'Close']
settleColumn = 'Close'
pivotColumn = 'Close'

# Variables
cal = USFederalHolidayCalendar()
pivotRange = 2
symbolDataArray = []
prevweekdayIndex = 0


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
    holidays = np.append(holidays, dt.datetime.strptime(bushHoliday, '%Y-%m-%d'))
    return holidays


# Get Previous Workday
def prev_weekday(adate, index):
    adate -= timedelta(days=index)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate


# Get Date Ranges
def get_date_ranges(date, pivotRange):
    today = prev_weekday(date, prevweekdayIndex)
    three_days_ago = today - BDay(pivotRange)
    startDate = three_days_ago.date()
    holidays = get_holidays(startDate, today)

    while dt.datetime.combine(startDate, dt.datetime.min.time()) in holidays:
        startDate = prev_weekday(startDate, 1)
    endDate = today
    return (startDate, endDate)


# Get Pivot Data
def get_pivot_data(symbol, startDate, endDate, columns):
    rawData = quandl.get(symbol, start_date=startDate, end_date=endDate)
    pivotData = rawData[columns]
    return pivotData


# Get Pivots
def get_three_day_pivots(pivotData, settle, noDigits):
    v1 = pivotData['High'].max()
    v2 = pivotData['Low'].min()
    v3 = settle

    pivot = round((v1 + v2 + v3) / 3, noDigits)
    pivotR1 = round((v1 + v2) / 2, noDigits)
    pivotR2 = round(((pivot - pivotR1) + pivot), noDigits)
    pivots = [pivot, pivotR1, pivotR2]
    return pivots


# Get Pivots
def get_pivots(pivotData, noDigits, settleColumn):
    v1 = pivotData['High'][0]
    v2 = pivotData['Low'][0]
    v3 = pivotData[settleColumn][0]

    pivot = round((v1 + v2 + v3) / 3, noDigits)
    pivotR1 = round((v1 + v2) / 2, noDigits)
    pivotR2 = round(((pivot - pivotR1) + pivot), noDigits)
    pivots = [pivot, pivotR1, pivotR2]
    return pivots


# Get Support Resistances
def get_support_resistances(pivotData, todayPivot, noDigits):
    # Daily Pivot Calculations
    todayMax = pivotData['High'].item()
    todayMin = pivotData['Low'].item()
    # Resistances and Supports
    todayR1 = round((2 * todayPivot) - todayMin, noDigits)
    todayS1 = round((2 * todayPivot) - todayMax, noDigits)
    todayR2 = round(todayPivot + (todayR1 - todayS1), noDigits)
    todayS2 = round(todayPivot - (todayR1 - todayS1), noDigits)
    todayR3 = round(todayMax + 2 * (todayPivot - todayMin), noDigits)
    todayS3 = round(todayMin - 2 * (todayMax - todayPivot), noDigits)
    todayR = [todayR1, todayR2, todayR3]
    todayS = [todayS1, todayS2, todayS3]
    return [*todayR, *todayS]


# Get Symbol Information
def get_symbol_data(symbol, date, noDigits):
    # Get Date Range
    startDate, endDate = get_date_ranges(date, pivotRange)

    # Get pivot data
    threeDayPivotData = get_pivot_data(symbol, startDate, endDate, columns)
    todayPivotData = get_pivot_data(symbol, endDate, endDate, columns)

    if (todayPivotData.empty):
        return np.array([np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                         np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                         np.NaN, np.NaN, np.NaN, np.NaN, np.NaN])
    else:
        # Three Day Pivots and Daily Pivots
        threeDayPivots = get_three_day_pivots(threeDayPivotData, todayPivotData[pivotColumn][0], noDigits)
        dailyPivots = get_pivots(todayPivotData, noDigits, settleColumn)
        supportResistance = get_support_resistances(todayPivotData, dailyPivots[0], noDigits)
        return np.array(
            [endDate, symbol, todayPivotData[pivotColumn][0], *threeDayPivots, *dailyPivots, *supportResistance])


# Get Price Data
def get_price_data(symbol, inputDate, numDays):
    inputDate = prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date(), prevweekdayIndex)
    # Get Date Range
    dateList = [inputDate - dt.timedelta(days=x) for x in range(0, int(numDays))]
    holidays = get_holidays(dateList[-1], dateList[0])

    priceDataArray = []
    timeDataArray = []

    for date in dateList:
        weekno = date.weekday()
        if weekno < 5:
            print("Getting Data for {}".format(date))
            if dt.datetime.combine(date, dt.datetime.min.time()) in holidays:
                print("Holiday {}".format(date))
            else:
                priceData = get_pivot_data(symbol, date, date, columns)
                if (priceData.empty):
                    print("Empty Data. Skipping for {}".format(inputDate))
                else:
                    timeDataArray.append(date)
                    priceDataArray.append(priceData[pivotColumn].item())
    return (timeDataArray, priceDataArray)


# Plot Chart
def plot_chart(xaxis, yaxis, p1, p11, p12, p2, p21, p22, s1, r1, s2, r2, s3, r3, fileName):
    # matplotlib.use('agg') - for lambda
    ax = pyplot.gca()
    xaxis = dates.date2num(xaxis)  # Convert to maplotlib format
    hfmt = dates.DateFormatter('%Y\n%m\n%d')
    ax.xaxis.set_major_formatter(hfmt)
    labelsize = 20
    fontsize = 16
    chartsize = 20
    linewidthchart = 4
    linewidthpivot = 4
    linewidthrange = 2

    pyplot.xlabel('date')
    pyplot.ylabel('price')
    pyplot.plot(xaxis, yaxis, linewidth=linewidthchart, color='black')
    pyplot.rcParams['font.size'] = labelsize
    xMid = (xaxis[0] + xaxis[-1]) / 2

    # 3 Day Pivot
    pyplot.axhline(y=p1, color='blue', linewidth=linewidthpivot, linestyle='dashed', label="3-day-pivot " + str(p1))
    pyplot.text(xMid, p1, p1, fontsize=fontsize, va='center', ha='center', backgroundcolor='w')
    pyplot.axhline(y=p11, color='blue', linewidth=linewidthrange, linestyle='-.', label="3-day-pivot-r1 " + str(p11))
    pyplot.axhline(y=p12, color='blue', linewidth=linewidthrange, linestyle='-.', label="3-day-pivot-r2 " + str(p12))

    # Daily Pivot
    pyplot.axhline(y=p2, color='grey', linewidth=linewidthpivot, linestyle='dashed', label="daily-pivot " + str(p2))
    pyplot.text(xMid, p2, p2, fontsize=fontsize, va='center', ha='center', backgroundcolor='w')
    pyplot.axhline(y=p21, color='grey', linestyle='-.', label="daily-pivot-r1 " + str(p21))
    pyplot.axhline(y=p22, color='grey', linestyle='-.', label="daily-pivot-r2 " + str(p22))

    # Support
    pyplot.axhline(y=s1, color='green', linestyle='dashed', label="support " + str(s1))
    # pyplot.text(xMid,s1,s1,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=s2, color='green', linestyle='dashed', label="support " + str(s2))
    # pyplot.text(xMid,s2,s2,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=s3, color='green', linestyle='dashed', label="support " + str(s3))
    # pyplot.text(xMid,s3,s3,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    # Resistance
    pyplot.axhline(y=r1, color='red', linestyle='dashed', label="resistance " + str(r1))
    # pyplot.text(xMid,r1,r1,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=r2, color='red', linestyle='dashed', label="resistance " + str(r2))
    # pyplot.text(xMid,r2,r2,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=r3, color='red', linestyle='dashed', label="resistance " + str(r3))
    # pyplot.text(xMid,r3,r3,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')

    # pyplot.rcParams['figure.figsize'] = 24, 24
    fig = pyplot.gcf()
    fig.set_size_inches(chartsize, chartsize)
    pyplot.legend()
    # pyplot.show()
    pyplot.savefig(fileName, bbox_inches='tight')
    return


# Prepare Data
def prepare_data(inputDate, numDays, symbol):
    startDate = prev_weekday(dt.datetime.strptime(inputDate, '%Y-%m-%d').date(), prevweekdayIndex)

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

    return symbolDataArray


# Check if path exists
def if_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


# Main function
def lambda_handler(event, context):
    # Set global variables
    global pivotColumn
    global settleColumn
    global columns

    # fileName = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')+'.csv'
    inputDate = os.environ.get("input_date")
    symbol = os.environ.get("symbol")
    chartDays = os.environ.get("num_days")
    symbolType = os.environ.get("symbol_type")
    if symbolType.upper() == 'F':
        pivotColumn = 'Last'
        settleColumn = 'Settle'
        columns = ['High', 'Low', 'Last', 'Settle']
    print("Symbol is -> {}".format(symbol))
    print("Input Date is -> {}".format(inputDate))
    print("Num Days is -> {}".format(numDays))
    print("Symbol Type is -> {}".format(symbolType))
    print("----------------------------")
    xaxis, yaxis = get_price_data(symbol, inputDate, chartDays)
    symbolPivotDataDF = pd.DataFrame(prepare_data(inputDate, numDays, symbol),
                                     columns=['Date', 'Symbol', 'Price', 'Pivot', 'PivotR1', 'PivotR2',
                                              'DPivot', 'DPivotR1', 'DPivotR2',
                                              'R1', 'R2', 'R3',
                                              'S1', 'S2', 'S3'
                                              ])
    pivot, pivotR1, pivotR2, dPivot, dPivotR1, dPivotR2, s1, r1, s2, r2, s3, r3 = (symbolPivotDataDF['Pivot'].item(),
                                                                                   symbolPivotDataDF['PivotR1'].item(),
                                                                                   symbolPivotDataDF['PivotR2'].item(),
                                                                                   symbolPivotDataDF['DPivot'].item(),
                                                                                   symbolPivotDataDF['DPivotR1'].item(),
                                                                                   symbolPivotDataDF['DPivotR2'].item(),
                                                                                   symbolPivotDataDF['S1'].item(),
                                                                                   symbolPivotDataDF['R1'].item(),
                                                                                   symbolPivotDataDF['S2'].item(),
                                                                                   symbolPivotDataDF['R2'].item(),
                                                                                   symbolPivotDataDF['S3'].item(),
                                                                                   symbolPivotDataDF['R3'].item(),
                                                                                   )
    # plot_file=outputDir+ntpath.basename(symbol)+dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')+'.png'
    plot_file_prefix = ntpath.basename(symbol) + dt.datetime.fromtimestamp(time.time()).strftime(
        '%Y-%m-%d-%H-%M-%S') + '.png'
    plot_file = lambda_path + plot_file_prefix
    plot_chart(xaxis, yaxis, pivot, pivotR1, pivotR2, dPivot, dPivotR1, dPivotR2, s1, r1, s2, r2, s3, r3, plot_file)
    # symbolPivotDataDF.to_csv(outputDir+fileName, sep=',', encoding='utf-8')
    print("Output Data is ->{}".format(symbolPivotDataDF))
    print("File Name is ->{}".format(plot_file_prefix))
    # Move chart to S3
    s3 = boto3.client('s3')
    s3.upload_file(plot_file, bucket_name, plot_file_prefix)
    return "Invocation Success"


# Generate ML data for all symbols in a file
def generate_ml_batch_data(inputFile, outputFile):
    print("Input File is -> {}".format(inputFile))
    inputDF = pd.read_csv(inputFile, header=None)
    for index, row in inputDF.iterrows():
        inputRow = inputDF[index:index + 1]
        symbol = inputRow[0].item()
        inputDate = inputRow[1].item()
        numDays = inputRow[2].item()
        print("----------------------------")
        print("Symbol -> {}".format(symbol))
        symbolPivotDataDF = generate_ml_data(symbol, inputDate, numDays)
    symbolPivotDataDF.to_csv(outputFile, sep=',', encoding='utf-8')
    return


# Generate ML data for 1 symbol
def generate_ml_data(symbol, inputDate, numDays):
    print("-----generate_ml_data-------")
    print("Symbol -> {}".format(symbol))
    symbolPivotDataDF = pd.DataFrame(
        prepare_data(inputDate, numDays, symbol),
        columns=['Date', 'Symbol', 'Price', 'Pivot', 'PivotR1', 'PivotR2',
                 'DPivot', 'DPivotR1', 'DPivotR2',
                 'R1', 'R2', 'R3',
                 'S1', 'S2', 'S3'
                 ])
    symbolPivotDataDF['Pivot'] = symbolPivotDataDF['Price'] - symbolPivotDataDF['Pivot']
    symbolPivotDataDF['PivotR1'] = symbolPivotDataDF['Price'] - symbolPivotDataDF['PivotR1']
    symbolPivotDataDF['PivotR2'] = symbolPivotDataDF['Price'] - symbolPivotDataDF['PivotR2']
    symbolPivotDataDF['DPivot'] = symbolPivotDataDF['Price'] - symbolPivotDataDF['DPivot']
    symbolPivotDataDF['DPivotR1'] = symbolPivotDataDF['Price'] - symbolPivotDataDF['DPivotR1']
    symbolPivotDataDF['DPivotR2'] = symbolPivotDataDF['Price'] - symbolPivotDataDF['DPivotR2']
    symbolPivotDataDF = symbolPivotDataDF.iloc[:, 0:9]
    print("----------------------------")
    return symbolPivotDataDF


# Generate Charts for specific symbol
def generate_charts(symbol, inputDate, chartDays, outputDir, fileName):
    print("-------generate_charts--------")
    print("Symbol -> {}".format(symbol))
    xaxis, yaxis = get_price_data(symbol, inputDate, chartDays)
    symbolPivotDataDF = pd.DataFrame(prepare_data(inputDate, numDays, symbol),
                                     columns=['Date', 'Symbol', 'Price', 'Pivot', 'PivotR1', 'PivotR2',
                                              'DPivot', 'DPivotR1', 'DPivotR2',
                                              'R1', 'R2', 'R3',
                                              'S1', 'S2', 'S3'
                                              ])
    if (np.isnan(symbolPivotDataDF['Price'][0])):
        print("Empty data returned for -> {}".format(inputDate))
    else:
        pivot, pivotR1, pivotR2, dPivot, dPivotR1, dPivotR2, s1, r1, s2, r2, s3, r3 = (
            symbolPivotDataDF['Pivot'].item(),
            symbolPivotDataDF['PivotR1'].item(),
            symbolPivotDataDF['PivotR2'].item(),
            symbolPivotDataDF['DPivot'].item(),
            symbolPivotDataDF['DPivotR1'].item(),
            symbolPivotDataDF['DPivotR2'].item(),
            symbolPivotDataDF['S1'].item(),
            symbolPivotDataDF['R1'].item(),
            symbolPivotDataDF['S2'].item(),
            symbolPivotDataDF['R2'].item(),
            symbolPivotDataDF['S3'].item(),
            symbolPivotDataDF['R3'].item(),
        )
        plot_file = outputDir + ntpath.basename(symbol) + dt.datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d-%H-%M-%S') + '.png'
        plot_chart(xaxis, yaxis, pivot, pivotR1, pivotR2, dPivot, dPivotR1, dPivotR2, s1, r1, s2, r2, s3, r3, plot_file)
        # symbolPivotDataDF.to_csv(outputDir+fileName, sep=',', encoding='utf-8')
    print("----------------------------")
    return


# Main function
def main(argv):
    fileName = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S') + '.csv'
    symbol = ''
    inputDate = ''
    symbolType = ''
    outputDir = 'output/'
    if_exists(outputDir)

    # Set global variables
    global pivotColumn
    global settleColumn
    global columns

    try:
        opts, args = getopt.getopt(argv, "hs:d:n:t:", ["symbol=", "date=", "days=", "type="])
    except getopt.GetoptError:
        print('quandlpivotchart.py -s <symbol> -d<date> -n <days> -t <type>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('quandlpivotchart.py -s <symbol> -d<date> -n <days> -t <type>')
            sys.exit()
        elif opt in ("-s", "--symbol"):
            symbol = arg
        elif opt in ("-d", "--date"):
            inputDate = arg
        elif opt in ("-n", "--days"):
            chartDays = arg
        elif opt in ("-t", "--type"):
            symbolType = arg
            if symbolType.upper() == 'F':
                pivotColumn = 'Last'
                settleColumn = 'Settle'
                columns = ['High', 'Low', 'Last', 'Settle']
        else:
            print("No arguments....")
            sys.exit(2)
    print("Symbol is -> {}".format(symbol))
    print("Input Date is -> {}".format(inputDate))
    print("Chart Days is -> {}".format(chartDays))
    print("Type is -> {}".format(symbolType))
    print("----------------------------")
    generate_charts(symbol, inputDate, chartDays, outputDir, fileName)
    # mlDF = generate_ml_data(symbol,inputDate,chartDays)
    # mlDF.to_csv(outputDir+fileName, sep=',', encoding='utf-8')
    # generate_ml_batch_data('input/symbolDump.csv',outputDir+fileName)


if __name__ == "__main__":
    main(sys.argv[1:])
