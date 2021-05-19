import pandas as pd
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt

SRC_DATA_FILENAME = '../sbin_data.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2009, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)

close = sbin_data['Close']

'''
The Absolute Price Oscillator (APO) is based on the absolute differences between two moving averages of different
lengths, a ‘Fast’ and a ‘Slow’ moving average.
APO = Fast Exponential Moving Average - Slow Exponential Moving Average
'''
num_periods_fast = 10  # time period for the fast EMA
k_fast = 2 / (num_periods_fast + 1)  # smoothing factor for fast EMA
ema_fast = 0
num_periods_slow = 40  # time period for the slow EMA
k_slow = 2 / (num_periods_slow + 1)  # smoothing factor for slow EMA
ema_slow = 0

ema_fast_values = []  # we will store fast EMA values for visualization purposes
ema_slow_values = []  # we will store slow EMA values for visualization purposes
apo_values = []  # track computed absolute price oscillator values
for close_price in close:
    if ema_fast == 0:  # first observation
        ema_fast = close_price
        ema_slow = close_price
    else:
        ema_fast = (close_price - ema_fast) * k_fast + ema_fast
        ema_slow = (close_price - ema_slow) * k_slow + ema_slow

    ema_fast_values.append(ema_fast)
    ema_slow_values.append(ema_slow)
    apo_values.append(ema_fast - ema_slow)

sbin_data = sbin_data.assign(ClosePrice=pd.Series(close, index=sbin_data.index))
sbin_data = sbin_data.assign(FastExponential10DayMovingAverage=pd.Series(ema_fast_values, index=sbin_data.index))
sbin_data = sbin_data.assign(SlowExponential40DayMovingAverage=pd.Series(ema_slow_values, index=sbin_data.index))
sbin_data = sbin_data.assign(AbsolutePriceOscillator=pd.Series(apo_values, index=sbin_data.index))

close_price = sbin_data['ClosePrice']
ema_f = sbin_data['FastExponential10DayMovingAverage']
ema_s = sbin_data['SlowExponential40DayMovingAverage']
apo = sbin_data['AbsolutePriceOscillator']

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel="SBI Price in Rs")
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ema_f.plot(ax=ax1, color='b', lw=2., legend=True)
ema_s.plot(ax=ax1, color='r', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='APO')
apo.plot(ax=ax2, color='black', lw=2., legend=True)
plt.show()
