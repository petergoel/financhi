# -*- coding: utf-8 -*-
import quandl
import logging

log = logging.getLogger(__name__)

quandl.ApiConfig.api_key = 'myUW3XaM4eC7WEzTXzZA'

# Get Pivot Data
def get_pivot_data(symbol, start_date, end_date, columns= ['High', 'Low', 'Close']):
    log.debug('get_pivot_data:: [input parameters] %s %s %s', symbol,start_date,end_date)
    raw_data = quandl.get(symbol, start_date=start_date, end_date=end_date)
    pivot_data = raw_data[columns]
    log.debug('get_pivot_data:: pivot data obtained is %s',pivot_data)
    return pivot_data


#Calculate Pivots
def calculate_pivots(v1,v2,v3,no_digits=2):
    pivot = round((v1 + v2 + v3) / 3, no_digits)
    pivot_r1 = round((v1 + v2) / 2, no_digits)
    pivot_r2 = round(((pivot - pivot_r1) + pivot), no_digits)
    pivots = [pivot, pivot_r1, pivot_r2]
    log.debug('calculate_pivots:: pivots  obtained are %s', pivots)
    return pivots


# Get Three Day Pivots
def get_three_day_pivots(pivot_data, settle, no_digits=2):
    if (pivot_data.empty):
        return []
    v1 = pivot_data['High'].max()
    v2 = pivot_data['Low'].min()
    v3 = settle
    log.debug('get_three_day_pivots:: v1, v2, v3 are : %s, %s, %s',v1,v2,v3)

    return calculate_pivots(v1,v2,v3,no_digits)


# Get Pivots
def get_pivots(pivot_data, settle_column='Close',no_digits=2):
    if(pivot_data.empty):
        return []
    v1 = pivot_data['High'].item()
    v2 = pivot_data['Low'].item()
    v3 = pivot_data[settle_column].item()
    log.debug('get_pivots:: v1, v2, v3 are : %s, %s, %s',v1,v2,v3)

    return calculate_pivots(v1, v2, v3, no_digits)


# Get Support Resistances
def get_support_resistances(pivot_data, today_pivot, no_digits=2):
    # Daily Pivot Calculations
    today_max = pivot_data['High'].item()
    today_min = pivot_data['Low'].item()

    # Resistances and Supports
    today_r1 = round((2 * today_pivot) - today_min, no_digits)
    today_s1 = round((2 * today_pivot) - today_max, no_digits)
    today_r2 = round(today_pivot + (today_r1 - today_s1), no_digits)
    today_s2 = round(today_pivot - (today_r1 - today_s1), no_digits)
    today_r3 = round(today_max + 2 * (today_pivot - today_min), no_digits)
    today_s3 = round(today_min - 2 * (today_max - today_pivot), no_digits)
    today_r = [today_r1, today_r2, today_r3]
    today_s = [today_s1, today_s2, today_s3]
    log.debug('calculate_pivots:: Resistances  obtained are %s', today_r)
    log.debug('calculate_pivots:: Supports  obtained are %s', today_s)

    return [*today_r, *today_s]
