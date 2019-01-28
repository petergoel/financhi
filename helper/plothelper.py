# -*- coding: utf-8 -*-
from matplotlib import pyplot, dates

# TODO - Optimize function
# Plot Chart
def plot_chart(xaxis, yaxis, p1, p11, p12, p2, p21, p22, s1, r1, s2, r2, s3, r3, fileName):
    # matplotlib.use('agg') - for lambda
    ax = pyplot.gca()
    xaxis = dates.date2num(xaxis)  # Convert to maplotlib format
    hfmt = dates.DateFormatter('%Y\n%m\n%d')
    ax.xaxis.set_major_formatter(hfmt)

    # Variables
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
    pyplot.clf()
    return


# Plot Chart
def plot_chart_pivots(xaxis, yaxis, p1, p2, p3, fileName):
    ax = pyplot.gca()
    xaxis = dates.date2num(xaxis)  # Convert to maplotlib format
    hfmt = dates.DateFormatter('%Y\n%m\n%d')
    ax.xaxis.set_major_formatter(hfmt)
    pyplot.xlabel('date')
    pyplot.ylabel('price')
    pyplot.plot(xaxis, yaxis, 'ro', color='blue', linewidth=2, linestyle='dashed', label='price')

    pyplot.plot(xaxis, p1, 'ro', color='red', linewidth=1, linestyle='dashed', label="3-day-pivot")
    pyplot.plot(xaxis, p2, 'bs', color='olive', linewidth=1, linestyle='dashed', label="3-day-pivot-R1")
    pyplot.plot(xaxis, p3, 'g^', color='olive', linewidth=1, linestyle='dashed', label="3-day-pivot-R2")

    pyplot.rcParams['figure.figsize'] = 20, 20
    pyplot.legend()
    pyplot.savefig(fileName, bbox_inches='tight')
    pyplot.clf()
    return