import pandas as pd
from nsepy import get_history
from datetime import date
import statistics as stats
import math as math
import matplotlib.pyplot as plt

SRC_DATA_FILENAME = '../sbin_data.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2009, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)

close = sbin_data['Close']

'''
The Bollinger Band (BBANDS) study created by John Bollinger plots upper and lower envelope bands around the price of the
instrument. The width of the bands is based on the standard deviation of the closing prices from a moving average of
price.
Middle Band = n-period moving average
Upper Band = Middle Band + ( y * n-period standard deviation)
Lower Band = Middle Band - ( y * n-period standard deviation)
Where:
n = number of periods
y = factor to apply to the standard deviation value, (typical default for y = 2)
'''

time_period = 20  # history length for Simple Moving Average for middle band
stdev_factor = 2  # Standard Deviation Scaling factor for the upper and lower bands
history = []  # price history for computing simple moving average
sma_values = []  # moving average of prices for visualization purposes
upper_band = []  # upper band values
lower_band = []  # lower band values

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:  # we only want to maintain at most 'time_period' number of price observations
        del (history[0])

    sma = stats.mean(history)
    sma_values.append(sma)  # simple moving average or middle band
    variance = 0  # variance is the square of standard deviation
    for hist_price in history:
        variance = variance + ((hist_price - sma) ** 2)
    stdev = math.sqrt(variance / len(history))  # use square root to get standard deviation
    upper_band.append(sma + stdev_factor * stdev)
    lower_band.append(sma - stdev_factor * stdev)

sbin_data = sbin_data.assign(ClosePrice=pd.Series(close, index=sbin_data.index))
sbin_data = sbin_data.assign(MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=sbin_data.index))
sbin_data = sbin_data.assign(UpperBollingerBand20DaySMA2StdevFactor=pd.Series(upper_band, index=sbin_data.index))
sbin_data = sbin_data.assign(LowerBollingerBand20DaySMA2StdevFactor=pd.Series(lower_band, index=sbin_data.index))

close_price = sbin_data['ClosePrice']
mband = sbin_data['MiddleBollingerBand20DaySMA']
uband = sbin_data['UpperBollingerBand20DaySMA2StdevFactor']
lband = sbin_data['LowerBollingerBand20DaySMA2StdevFactor']

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI Price in Rs')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
mband.plot(ax=ax1, color='b', lw=2., legend=True)
uband.plot(ax=ax1, color='black', lw=2., legend=True)
lband.plot(ax=ax1, color='r', lw=2., legend=True)
plt.show()
