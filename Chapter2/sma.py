import pandas as pd
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
import statistics as stats

SRC_DATA_FILENAME = '../sbin_data.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2009, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)

close = sbin_data['Close']

'''
Simple Moving Average
SMA = ( Sum ( Price, n ) ) / n    
Where: n = Time Period
'''

time_period = 20  # number of days over which to average
history = []  # to track a history of prices
sma_values = []  # to track SMA values

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:  # we remove oldest price because we only average over last 'time_period' prices
        del(history[0])
    sma_values.append(stats.mean(history))

sbin_data = sbin_data.assign(ClosePrice=pd.Series(close, index=sbin_data.index))
sbin_data = sbin_data.assign(Simple20DayMovingAverage=pd.Series(sma_values, index=sbin_data.index))

close_price = sbin_data['ClosePrice']
sma = sbin_data['Simple20DayMovingAverage']

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI Price in Rs')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
sma.plot(ax=ax1, color='r', lw=2., legend=True)
plt.show()
