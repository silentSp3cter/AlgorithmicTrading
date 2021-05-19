import pandas as pd
import matplotlib.pyplot as plt
from nsepy import get_history
from datetime import date

SRC_DATA_FILENAME = '../sbin_data.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2009, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)

close = sbin_data['Close']

'''
The Exponential Moving Average (EMA) represents an average of prices, but places more weight on recent prices. The
weighting applied to the most recent price depends on the selected period of the moving average. The shorter the period
for the EMA, the more weight that will be applied to the most recent price.

EMA = ( P - EMAp ) * K + EMAp

Where:
P = Price for the current period
EMAp = the Exponential moving Average for the previous period
K = the smoothing constant, equal to 2 / (n + 1)
n = the number of periods in a simple moving average roughly approximated by the EMA
'''

num_periods = 20  # number of dats over which to average
k = 2 / (num_periods + 1)  # smoothing constant
ema_p = 0
ema_values = []  # to hold computed EMA values

for close_price in close:
    if ema_p == 0:  # first observation, EMA = current-price
        ema_p = close_price
    else:
        ema_p = (close_price - ema_p) * k + ema_p

    ema_values.append(ema_p)

sbin_data = sbin_data.assign(ClosePrice=pd.Series(close, index=sbin_data.index))
sbin_data = sbin_data.assign(Exponential20DayMovingAverage=pd.Series(ema_values, index=sbin_data.index))

close_price = sbin_data['ClosePrice']
ema = sbin_data['Exponential20DayMovingAverage']

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI Price in Rs')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ema.plot(ax=ax1, color='b', lw=2., legend=True)
plt.show()
