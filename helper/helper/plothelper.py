# -*- coding: utf-8 -*-
from matplotlib import pyplot
import numpy as np
from matplotlib.ticker import Formatter


class MyFormatter(Formatter):
    def __init__(self, dates, fmt='%Y-%m-%d'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        ind = int(np.round(x))
        if ind >= len(self.dates) or ind < 0:
            return ''

        return self.dates[ind].strftime(self.fmt)


# TODO - Optimize function
# Plot Chart
def plot_chart(xaxis, yaxis, p1, p11, p12, p2, p21, p22, s1, r1, s2, r2, s3, r3, fileName):
    # matplotlib.use('agg') - for lambda
    ax = pyplot.gca()
    # xaxis = dates.date2num(xaxis)    # Convert to maplotlib format
    # hfmt = dates.DateFormatter('%Y\n%m\n%d')
    # ax.xaxis.set_major_formatter(hfmt)

    formatter = MyFormatter(xaxis[::-1])
    ax.xaxis.set_major_formatter(formatter)

    labelsize = 20
    fontsize = 16
    chartsize = 20
    linewidthchart = 4
    linewidthpivot = 4
    linewidthrange = 2
    markersize = 20

    pyplot.xlabel('date')
    pyplot.ylabel('price')

    xscale = np.arange(len(xaxis))
    xscale = xscale[::-1]

    pyplot.plot(xscale, yaxis, marker='o', markersize=markersize, linewidth=linewidthchart, color='black')
    pyplot.rcParams['font.size'] = labelsize
    # xMid = (xaxis[0] + xaxis[-1]) / 2

    # 3 Day Pivot
    pyplot.axhline(y=p1, color='blue', linewidth=linewidthpivot, linestyle='dashed', label="3-day-pivot " + str(p1))
    # pyplot.text(xMid, p1, p1, fontsize=fontsize, va='center', ha='center', backgroundcolor='w')
    pyplot.axhline(y=p11, color='blue', linewidth=linewidthrange, linestyle='-.', label="3-day-pivot-r1 " + str(p11))
    pyplot.axhline(y=p12, color='blue', linewidth=linewidthrange, linestyle='-.', label="3-day-pivot-r2 " + str(p12))

    # Daily Pivot
    pyplot.axhline(y=p2, color='grey', linewidth=linewidthpivot, linestyle='dashed', label="daily-pivot " + str(p2))
    # pyplot.text(xMid, p2, p2, fontsize=fontsize, va='center', ha='center', backgroundcolor='w')
    pyplot.axhline(y=p21, color='grey', linestyle='-.', label="daily-pivot-r1 " + str(p21))
    pyplot.axhline(y=p22, color='grey', linestyle='-.', label="daily-pivot-r2 " + str(p22))

    # Support
    pyplot.axhline(y=s1, color='green', linestyle='dashed', label="support 1 " + str(s1))
    # pyplot.text(xMid,s1,s1,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=s2, color='green', linestyle='dashed', label="support 2 " + str(s2))
    # pyplot.text(xMid,s2,s2,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=s3, color='green', linestyle='dashed', label="support 3 " + str(s3))
    # pyplot.text(xMid,s3,s3,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    # Resistance
    pyplot.axhline(y=r1, color='red', linestyle='dashed', label="resistance 1 " + str(r1))
    # pyplot.text(xMid,r1,r1,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=r2, color='red', linestyle='dashed', label="resistance 2 " + str(r2))
    # pyplot.text(xMid,r2,r2,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    pyplot.axhline(y=r3, color='red', linestyle='dashed', label="resistance 3 " + str(r3))
    # pyplot.text(xMid,r3,r3,fontsize=fontsize, va='center', ha='center',backgroundcolor='w')
    # pyplot.xticks(rotation=90)

    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)
    fig = pyplot.gcf()
    fig.set_size_inches(chartsize, chartsize)
    fig.autofmt_xdate()

    pyplot.legend()
    pyplot.savefig(fileName, bbox_inches='tight')
    pyplot.clf()
    return


# Plot Chart
def plot_chart_pivots(xaxis, yaxis, p1, p2, fileName):
    ax = pyplot.gca()
    # xaxis = dates.date2num(xaxis)    # Convert to maplotlib format
    # hfmt = dates.DateFormatter('%Y\n%m\n%d')
    # ax.xaxis.set_major_formatter(hfmt)

    formatter = MyFormatter(xaxis[::-1])
    ax.xaxis.set_major_formatter(formatter)

    labelsize = 20
    # fontsize = 16
    chartsize = 20
    linewidthchart = 4
    linewidthrange = 2
    markersize = 20

    pyplot.xlabel('date')
    pyplot.ylabel('price')
    pyplot.rcParams['font.size'] = labelsize

    xscale = np.arange(len(xaxis))
    xscale = xscale[::-1]
    pyplot.plot(xscale, yaxis, marker='o', markersize=markersize, color='black', linewidth=linewidthchart,
                label='price ' + str(yaxis[0]))
    pyplot.plot(xscale, p1, marker='o', markersize=markersize, color='blue', linewidth=linewidthrange,
                linestyle='dashed', label="3-day-pivot " + str(p1[0]))
    pyplot.plot(xscale, p2, marker='o', markersize=markersize, color='grey', linewidth=linewidthrange,
                linestyle='dashed', label="daily-pivot " + str(p2[0]))
    # pyplot.xticks(rotation=90)

    # for xc in dates.date2num(xaxis):
    #   pyplot.axvline(x=xc,color='olive', linestyle='dashed')

    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)

    fig = pyplot.gcf()
    fig.set_size_inches(chartsize, chartsize)
    fig.autofmt_xdate()

    # pyplot.rcParams['figure.figsize'] = chartsize, chartsize
    pyplot.legend()
    pyplot.savefig(fileName, bbox_inches='tight')
    pyplot.clf()
    return
