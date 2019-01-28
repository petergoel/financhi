import helper
import logging
import pandas as pd
import numpy as np
import ntpath
import datetime as dt
import time


# Generate Charts for specific symbol
def generate_charts(symbol, inputDate, chartDays, outputDir, fileName,numDays,prev_weekday_index,noDigits,columns,pivotColumn,settleColumn):
    print("-------generate_charts--------")
    print("Symbol -> {}".format(symbol))
    xaxis, yaxis = helper.financhi.get_price_data(symbol, inputDate, chartDays,prev_weekday_index,columns,pivotColumn)
    symbolPivotDataDF = pd.DataFrame(helper.financhi.prepare_data(inputDate, numDays, symbol,prev_weekday_index,noDigits,columns,pivotColumn,settleColumn),
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
        helper.plothelper.plot_chart(xaxis, yaxis, pivot, pivotR1, pivotR2, dPivot, dPivotR1, dPivotR2, s1, r1, s2, r2, s3, r3, plot_file)
        # symbolPivotDataDF.to_csv(outputDir+fileName, sep=',', encoding='utf-8')
    print("----------------------------")
    return

# Generate ML data for all symbols in a file
def generate_ml_batch_data(inputFile, outputFile,prev_weekday_index,noDigits,columns,pivotColumn,settleColumn):
    print("Input File is -> {}".format(inputFile))
    inputDF = pd.read_csv(inputFile, header=None)
    for index, row in inputDF.iterrows():
        inputRow = inputDF[index:index + 1]
        symbol = inputRow[0].item()
        inputDate = inputRow[1].item()
        numDays = inputRow[2].item()
        print("----------------------------")
        print("Symbol -> {}".format(symbol))
        symbolPivotDataDF = generate_ml_data(symbol, inputDate, numDays,prev_weekday_index,noDigits,columns,pivotColumn,settleColumn)
    symbolPivotDataDF.to_csv(outputFile, sep=',', encoding='utf-8')
    return


# Generate ML data for 1 symbol
def generate_ml_data(symbol, inputDate, numDays,prev_weekday_index,noDigits,columns,pivotColumn,settleColumn):
    print("-----generate_ml_data-------")
    print("Symbol -> {}".format(symbol))
    symbolPivotDataDF = pd.DataFrame(
        helper.financhi.prepare_data(inputDate, numDays, symbol,prev_weekday_index,noDigits,columns,pivotColumn,settleColumn),
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