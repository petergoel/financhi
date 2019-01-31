# -*- coding: utf-8 -*-
import helper
import logging
import unittest
import pandas as pd
import ntpath
import datetime as dt
import time
import os

logger = logging.getLogger(__name__)
pd.set_option('display.expand_frame_repr', False)


def if_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


class BasicTestSuite(unittest.TestCase):
    def test_get_pivot_data(self):
        # Variables
        symbol = 'CHRIS/CME_ES1'
        input_date = '2019-01-02'
        num_days = 20
        output_dir = '../output/'
        extension_csv='.csv'
        extension_json='.json'
        file_name = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        csv_file_name = output_dir + ntpath.basename(symbol) + '_' + file_name + extension_csv
        json_file_name = output_dir + ntpath.basename(symbol) + '_' + file_name + extension_json
        if_exists(output_dir)

        start_date, end_date = helper.get_start_date(input_date, num_days)
        logger.debug('test_get_pivot_data:: start_date is : %s', start_date)
        logger.debug('test_get_pivot_data:: end_date is : %s', end_date)
        columns = ['High', 'Low', 'Last', 'Settle']
        logger.debug("Holidays %s", helper.get_holidays(start_date,end_date))
        logger.debug("Number of Holidays %s", len(helper.get_holidays(start_date,end_date)))


        logger.debug('test_get_pivot_data:: Input Parameters [ %s, %s, %s, %s ]', symbol, start_date, end_date, columns)
        pivot_data = helper.get_pivot_data(symbol, start_date, end_date, columns)
        symbol_df = pd.DataFrame(pivot_data).reset_index()
        symbol_df.columns = ['Date', 'High', 'Low', 'Last', 'Settle']
        symbol_df['Date'] = symbol_df['Date'].dt.strftime('%Y-%m-%d')
        symbol_df['Symbol'] = ntpath.basename(symbol)
        # logger.debug('test_get_pivot_data:: symbol_df obtained are %s', symbol_df)

        self.assertEqual(pivot_data.empty, False)

        pivot_df = self.get_pivot_data(symbol_df)
        pivot_df = self.get_three_day_pivot_data(symbol_df, pivot_df)
        pivot_df = pivot_df.drop(['Pivot'], axis=1)
        # logger.debug(pivot_df)
        pivot_df.to_csv(csv_file_name, sep=',', encoding='utf-8')
        with open(json_file_name, 'w') as f:
            f.write(pivot_df.to_json(orient='records', lines=True))


    def get_pivot_data(self, df):
        settle_column = 'Settle'
        logger.debug("***********************")
        pivot_data_list = []
        for index, row in df.iloc[::-1].iterrows():
            input_row = df[index:index + 1]
            daily_pivots = helper.get_pivots(input_row, settle_column)
            support_resistance = helper.get_support_resistances(input_row, daily_pivots[0])
            # logger.debug('get_pivot_data:: Daily Pivots for %s : %s', input_row['Date'].item(), daily_pivots)
            # logger.debug('get_pivot_data:: Support Resistance for %s : %s', input_row['Date'].item(),support_resistance)
            pivot_data_list.append(
                [input_row['Date'].item(), input_row['Symbol'].item(), input_row['Last'].item(), *daily_pivots,
                 *support_resistance])
        pivot_df = pd.DataFrame(pivot_data_list,
                                columns=['Date', 'Symbol', 'Price', 'DPivot', 'DPivotR1', 'DPivotR2', 'S1', 'S2', 'S3',
                                         'R1',
                                         'R2',
                                         'R3'])
        logger.debug('get_pivot_data:: pivot_df is %s', pivot_df)
        return pivot_df

    def get_three_day_pivot_data(self, df, pivot_df):
        settle_column = 'Settle'
        pivot_column = 'Last'
        pivot_constant = 2
        three_day_pivot_data_list = []
        three_day_pivot_df = df
        logger.debug("***********************")
        for index, row in df.iloc[::-1].iterrows():
            input_row = df[index:index + 1]
            if (index - pivot_constant >= 0):
                temp_three_day_df = three_day_pivot_df.iloc[[index, index - 1, index - 2]]
                # logger.debug('get_three_day_pivot_data:: temp_three_day_df is %s', temp_three_day_df)
                three_day_pivots = helper.get_three_day_pivots(temp_three_day_df, input_row[pivot_column].item())
                three_day_pivot_data_list.append([*three_day_pivots])
                logger.debug('get_three_day_pivot_data:: Three Day Pivots for %s : %s', input_row['Date'].item(),
                             three_day_pivots)
        logger.debug("get_three_day_pivot_data:: 3d pivot list %s", three_day_pivot_data_list)

        pivot_df.drop(pivot_df.tail(pivot_constant).index, inplace=True)  # Remove First 2 rows
        # pivot_df = pivot_df.iloc[::-1]
        pivot_df['Pivot'] = three_day_pivot_data_list
        pivot_df_detail = pd.DataFrame(pivot_df)
        pivot_df_detail[['3DPivot', '3DPivotR1', '3DPivotR2']] = pd.DataFrame(pivot_df_detail.Pivot.values.tolist(),
                                                                              index=pivot_df_detail.index)
        return pivot_df_detail


if __name__ == '__main__':
    unittest.main()
