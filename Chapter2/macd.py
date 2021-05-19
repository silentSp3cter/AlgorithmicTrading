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
The Moving Average Convergence Divergence (MACD) is based on the differences between two moving averages of different
lengths, a Fast and a Slow moving average. A second line, called the Signal line is plotted as a moving average of the 
MACD. A third line, called the MACD Histogram is optionally plotted as a histogram of the difference between the MACD 
and the Signal Line.

MACD = FastMA - SlowMA

Where:
FastMA is the shorter moving average and SlowMA is the longer moving average.
SignalLine = MovAvg (MACD)
MACD Histogram = MACD - SignalLine
 '''

num_periods_fast = 10  # fast EMA time period
K_fast = 2 / (num_periods_fast + 1)  # fast EMA smoothing factor
ema_fast = 0
num_periods_slow = 40  # slow EMA time period
K_slow = 2 / (num_periods_slow + 1)  # slow EMA smoothing factor
ema_slow = 0
num_periods_macd = 20  # MACD EMA time period
K_macd = 2 / (num_periods_macd + 1)  # MACD EMA smoothing factor
ema_macd = 0
ema_fast_values = []  # track fast EMA values for visualization purposes
ema_slow_values = []  # track slow EMA values for visualization purposes
macd_values = []  # track MACD values for visualization purposes
macd_signal_values = []  # MACD EMA values tracker
macd_histogram_values = []  # MACD - MACD-EMA
for close_price in close:
    if ema_fast == 0:  # first observation
        ema_fast = close_price
        ema_slow = close_price
    else:
        ema_fast = (close_price - ema_fast) * K_fast + ema_fast
        ema_slow = (close_price - ema_slow) * K_slow + ema_slow

    ema_fast_values.append(ema_fast)
    ema_slow_values.append(ema_slow)

    macd = ema_fast - ema_slow  # MACD is fast_MA - slow_EMA
    if ema_macd == 0:
        ema_macd = macd
    else:
        ema_macd = (macd - ema_macd) * K_macd + ema_macd  # signal is EMA of MACD values

    macd_values.append(macd)
    macd_signal_values.append(ema_macd)
    macd_histogram_values.append(macd - ema_macd)

sbin_data = sbin_data.assign(ClosePrice=pd.Series(close, index=sbin_data.index))
sbin_data = sbin_data.assign(FastExponential10DayMovingAverage=pd.Series(ema_fast_values, index=sbin_data.index))
sbin_data = sbin_data.assign(SlowExponential40DayMovingAverage=pd.Series(ema_slow_values, index=sbin_data.index))
sbin_data = sbin_data.assign(MovingAverageConvergenceDivergence=pd.Series(macd_values, index=sbin_data.index))
sbin_data = sbin_data.assign(Exponential20DayMovingAverageOfMACD=pd.Series(macd_signal_values, index=sbin_data.index))
sbin_data = sbin_data.assign(MACDHistogram=pd.Series(macd_histogram_values, index=sbin_data.index))

close_price = sbin_data['ClosePrice']
ema_f = sbin_data['FastExponential10DayMovingAverage']
ema_s = sbin_data['SlowExponential40DayMovingAverage']
macd = sbin_data['MovingAverageConvergenceDivergence']
ema_macd = sbin_data['Exponential20DayMovingAverageOfMACD']
macd_histogram = sbin_data['MACDHistogram']

fig = plt.figure()
ax1 = fig.add_subplot(311, ylabel='SBI price in Rs')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ema_f.plot(ax=ax1, color='b', lw=2., legend=True)
ema_s.plot(ax=ax1, color='r', lw=2., legend=True)
ax2 = fig.add_subplot(312, ylabel='MACD')
macd.plot(ax=ax2, color='black', lw=2., legend=True)
ema_macd.plot(ax=ax2, color='g', lw=2., legend=True)
ax3 = fig.add_subplot(313, ylabel='MACD')
macd_histogram.plot(ax=ax3, color='r', kind='bar', legend=True, use_index=False)
plt.show()
