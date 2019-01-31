# -*- coding: utf-8 -*-
from matplotlib import pyplot, dates
import logging
import datetime as dt

logger = logging.getLogger(__name__)

# Chart variables
labelsize = 24
chartsize = 32
fontsize=20
linewidthchart = 4
linewidthpivot = 4
linewidthrange = 2
markersize = 20


# Plot 3D and Daily Pivots along with Price for given interval

def plot_chart_pivots(pivot_df, file_name):
    date_list = pivot_df['Date']
    yaxis = pivot_df['Price']
    three_day_pivot = pivot_df['3DPivot']
    three_day_pivot_r1 = pivot_df['3DPivotR1']
    three_day_pivot_r2 = pivot_df['3DPivotR2']
    daily_pivot = pivot_df['DPivot']
    daily_pivot_r1 = pivot_df['DPivotR1']
    daily_pivot_r2 = pivot_df['DPivotR2']
    daily_s1 = pivot_df['S1']
    daily_s2 = pivot_df['S2']
    daily_s3 = pivot_df['S3']
    daily_r1 = pivot_df['R1']
    daily_r2 = pivot_df['R2']
    daily_r3 = pivot_df['R3']
    symbol=pivot_df['Symbol']

    logger.debug("[xaxis, yaxis] [ %s, %s]", date_list, yaxis)
    logger.debug("[pivot, pivotr1, pivotr2] [ %s, %s %s]", daily_pivot, daily_pivot_r1, daily_pivot_r2)
    logger.debug("[3dpivot, 3dpivotr1, 3dpivotr2] [ %s, %s %s]", three_day_pivot, three_day_pivot_r1,
                 three_day_pivot_r2)
    logger.debug("[s1, s2, s3] [ %s, %s %s]", daily_s1, daily_s2, daily_s3)
    logger.debug("[r1, r2, r3] [ %s, %s %s]", daily_r1, daily_r2, daily_r3)

    converted_dates = list(map(dt.datetime.strptime, date_list, len(date_list) * ['%Y-%m-%d']))
    xaxis = converted_dates
    ax = pyplot.gca()
    hfmt = dates.DateFormatter('%Y\n%m\n%d')
    ax.xaxis.set_major_formatter(hfmt)

    # Plot 1
    pyplot.subplot(1, 2, 1)
    pyplot.xlabel('date',fontsize=fontsize)
    pyplot.ylabel('price',fontsize=fontsize)
    pyplot.title(symbol[0] + "  Price vs. Pivots",fontsize=fontsize)
    pyplot.rcParams['font.size'] = labelsize

    pyplot.plot(xaxis, yaxis, marker='o', markersize=markersize, color='black', linewidth=linewidthchart,
                label='price ' + str(yaxis[0]))
    pyplot.plot(xaxis, three_day_pivot, marker='o', markersize=markersize, color='blue', linewidth=linewidthrange,
                linestyle='dashed', label="3-day-pivot " + str(three_day_pivot[0]))
    pyplot.plot(xaxis, daily_pivot, marker='o', markersize=markersize, color='grey', linewidth=linewidthrange,
                linestyle='dashed', label="daily-pivot " + str(daily_pivot[0]))

#    for xc in dates.date2num(xaxis):
#        pyplot.axvline(x=xc, color='olive', linestyle='dashed')

    fig1 = pyplot.gcf()
    fig1.set_size_inches(chartsize, chartsize)
    fig1.autofmt_xdate()
    pyplot.legend()

    # Plot 2
    pyplot.subplot(1, 2, 2)
    pyplot.xlabel('date', fontsize=fontsize)
    pyplot.ylabel('price', fontsize=fontsize)
    pyplot.title(symbol[0] + "  Support, Resistance and Pivots", fontsize=fontsize)
    pyplot.rcParams['font.size'] = labelsize

    pyplot.plot(xaxis, yaxis, marker='o', markersize=markersize, linewidth=linewidthchart, color='black')
    # 3 Day Pivot
    pyplot.axhline(y=three_day_pivot[0], color='blue', linewidth=linewidthpivot, linestyle='dashed',
                   label="3-day-pivot " + str(three_day_pivot[0]))
    pyplot.axhline(y=three_day_pivot_r1[0], color='blue', linewidth=linewidthrange, linestyle='-.',
                   label="3-day-pivot-r1 " + str(three_day_pivot_r1[0]))
    pyplot.axhline(y=three_day_pivot_r2[0], color='blue', linewidth=linewidthrange, linestyle='-.',
                   label="3-day-pivot-r2 " + str(three_day_pivot_r2[0]))

    # Daily Pivot
    pyplot.axhline(y=daily_pivot[0], color='grey', linewidth=linewidthpivot, linestyle='dashed',
                   label="daily-pivot " + str(daily_pivot[0]))
    pyplot.axhline(y=daily_pivot_r1[0], color='grey', linestyle='-.', label="daily-pivot-r1 " + str(daily_pivot_r1[0]))
    pyplot.axhline(y=daily_pivot_r2[0], color='grey', linestyle='-.', label="daily-pivot-r2 " + str(daily_pivot_r2[0]))

    # Support
    pyplot.axhline(y=daily_s1[0], color='green', linestyle='dashed', label="support 1 " + str(daily_s1[0]))
    pyplot.axhline(y=daily_s2[0], color='green', linestyle='dashed', label="support 2 " + str(daily_s2[0]))
    pyplot.axhline(y=daily_s3[0], color='green', linestyle='dashed', label="support 3 " + str(daily_s3[0]))

    # Resistance
    pyplot.axhline(y=daily_r1[0], color='red', linestyle='dashed', label="resistance 1 " + str(daily_r1[0]))
    pyplot.axhline(y=daily_r2[0], color='red', linestyle='dashed', label="resistance 2 " + str(daily_r2[0]))
    pyplot.axhline(y=daily_r3[0], color='red', linestyle='dashed', label="resistance 3 " + str(daily_r3[0]))

    fig2 = pyplot.gcf()
    fig2.set_size_inches(chartsize, chartsize)
    fig2.autofmt_xdate()

    pyplot.legend()
    pyplot.savefig(file_name, bbox_inches='tight')
    pyplot.clf()
    return
