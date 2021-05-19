import pandas as pd
import matplotlib.pyplot as plt
from nsepy import get_history
from datetime import date
import statistics as stats
import math as math

SRC_DATA_FILENAME = '../sbin_data.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2009, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)

close = sbin_data['Close']

time_period = 20  # look back period
history = []  # history of prices
sma_values = []  # to track moving average values for visualization purposes
stddev_values = []  # history of computed stdev values

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:  # we track at most 'time_period' number of prices
        del (history[0])
    sma = stats.mean(history)
    sma_values.append(sma)
    variance = 0  # variance is square of standard deviation
    for hist_price in history:
        variance = variance + ((hist_price - sma) ** 2)
    stdev = math.sqrt(variance / len(history))
    stddev_values.append(stdev)

sbin_data = sbin_data.assign(ClosePrice=pd.Series(close, index=sbin_data.index))
sbin_data = sbin_data.assign(StandardDeviationOver20Days=pd.Series(stddev_values, index=sbin_data.index))
close_price = sbin_data['ClosePrice']
stddev = sbin_data['StandardDeviationOver20Days']

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel='SBI price in Rs')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='Stddev in Rs')
stddev.plot(ax=ax2, color='b', lw=2., legend=True)
ax2.axhline(y=stats.mean(stddev_values), color='k')
plt.show()
