# -*- coding: utf-8 -*-
import logging
import pandas as pd
import ntpath
from . import quandlhelper
from . import charthelper

logger = logging.getLogger(__name__)


# Generate pyplot charts
def generate_charts(df, file):
    logger.debug("----generate_charts------")
    charthelper.plot_chart_pivots(df, file)


# Get Daily Pivot, Support, Resistance for all days
def calculate_pivot_data(df, settle_column='Close',pivot_column='Close'):
    pivot_data_list = []
    logger.debug("----calculate_pivot_data------")
    for index, row in df.iloc[::-1].iterrows():
        input_row = df[index:index + 1]
        daily_pivots = quandlhelper.get_pivots(input_row, settle_column)
        support_resistance = quandlhelper.get_support_resistances(input_row, daily_pivots[0])
        logger.debug('calculate_pivot_data:: Daily Pivots for [ %s ]  %s', input_row['Date'].item(), daily_pivots)
        logger.debug('calculate_pivot_data:: Support Resistance for [ %s ] %s', input_row['Date'].item(),
                     support_resistance)
        pivot_data_list.append(
            [input_row['Date'].item(), input_row['Symbol'].item(), input_row[pivot_column].item(), *daily_pivots,
             *support_resistance])
    pivot_df = pd.DataFrame(pivot_data_list,
                            columns=['Date', 'Symbol', 'Price', 'DPivot', 'DPivotR1', 'DPivotR2', 'R1', 'R2', 'R3',
                                     'S1',
                                     'S2',
                                     'S3'])
    # logger.debug('calculate_pivot_data:: pivot_df is %s', pivot_df)
    logger.debug("-------------------------")
    return pivot_df


# Get 3D Pivots for all days
def calculate_three_day_pivot_data(df, pivot_df, pivot_column='Close'):
    pivot_constant = 2
    three_day_pivot_data_list = []
    three_day_pivot_df = df
    logger.debug("----calculate_three_day_pivot_data------")
    for index, row in df.iloc[::-1].iterrows():
        input_row = df[index:index + 1]
        if (index - pivot_constant >= 0):
            temp_three_day_df = three_day_pivot_df.iloc[[index, index - 1, index - 2]]
            # logger.debug('calculate_three_day_pivot_data:: temp_three_day_df is %s', temp_three_day_df)
            three_day_pivots = quandlhelper.get_three_day_pivots(temp_three_day_df, input_row[pivot_column].item())
            three_day_pivot_data_list.append([*three_day_pivots])
            logger.debug('calculate_three_day_pivot_data:: Three Day Pivots for [ %s ] %s', input_row['Date'].item(),
                         three_day_pivots)
    # logger.debug("calculate_three_day_pivot_data:: 3d pivot list %s", three_day_pivot_data_list)

    pivot_df.drop(pivot_df.tail(pivot_constant).index, inplace=True)  # Remove First 2 rows
    pivot_df['Pivot'] = three_day_pivot_data_list
    pivot_df_detail = pd.DataFrame(pivot_df)
    pivot_df_detail[['3DPivot', '3DPivotR1', '3DPivotR2']] = pd.DataFrame(pivot_df_detail.Pivot.values.tolist(),
                                                                          index=pivot_df_detail.index)
    logger.debug("-------------------------")
    return pivot_df_detail


def run_financhi(symbol, start_date, end_date, columns=['High', 'Low', 'Close'],
                 futures_columns=['Date', 'High', 'Low', 'Close'], settle_column='Close', pivot_column='Close'):
    # get quandl data for pivots
    pivot_data = quandlhelper.get_pivot_data(symbol, start_date, end_date, columns)

    # Output from Quandl
    symbol_df = pd.DataFrame(pivot_data).reset_index()
    symbol_df.columns = futures_columns
    symbol_df['Date'] = symbol_df['Date'].dt.strftime('%Y-%m-%d')
    symbol_df['Symbol'] = ntpath.basename(symbol)
    logger.debug('run_financhi:: symbol_df rows obtained is [ %s ]', symbol_df.size)

    # get daily and 3 day pivots
    pivot_df = calculate_pivot_data(symbol_df, settle_column,pivot_column)
    pivot_df = calculate_three_day_pivot_data(symbol_df, pivot_df, pivot_column)
    pivot_df = pivot_df.drop(['Pivot'], axis=1)
    logger.debug('run_financhi:: pivot_df rows obtained is [ %s ]', pivot_df.size)

    return pivot_df
