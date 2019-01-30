# -*- coding: utf-8 -*-
import quandl
import logging

log = logging.getLogger(__name__)

quandl.ApiConfig.api_key = 'myUW3XaM4eC7WEzTXzZA'

# Get Pivot Data
def get_pivot_data(symbol, startDate, endDate, columns= ['High', 'Low', 'Close']):
    log.debug('[input parameters] %s %s %s', symbol,startDate,endDate)
    rawData = quandl.get(symbol, start_date=startDate, end_date=endDate)
    pivotData = rawData[columns]
    log.debug('pivot data obtained is',pivotData)
    return pivotData


# Get Three Day Pivots
def get_three_day_pivots(pivotData, settle, noDigits=2):
    if (pivotData.empty):
        return []
    v1 = pivotData['High'].max()
    v2 = pivotData['Low'].min()
    v3 = settle

    pivot = round((v1 + v2 + v3) / 3, noDigits)
    pivotR1 = round((v1 + v2) / 2, noDigits)
    pivotR2 = round(((pivot - pivotR1) + pivot), noDigits)
    pivots = [pivot, pivotR1, pivotR2]
    return pivots


# Get Pivots
def get_pivots(pivotData, settleColumn='Close',noDigits=2):
    if(pivotData.empty):
        return []
    v1 = pivotData['High'][0]
    v2 = pivotData['Low'][0]
    v3 = pivotData[settleColumn][0]

    pivot = round((v1 + v2 + v3) / 3, noDigits)
    pivotR1 = round((v1 + v2) / 2, noDigits)
    pivotR2 = round(((pivot - pivotR1) + pivot), noDigits)
    pivots = [pivot, pivotR1, pivotR2]
    return pivots


# Get Support Resistances
def get_support_resistances(pivotData, todayPivot, noDigits=2):
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
