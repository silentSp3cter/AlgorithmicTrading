from nsepy import get_history
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SRC_DATA_FILENAME = '../sbin_data.pickle'
# Reading SBI stock data from 01-01-2009 to 01-01-2013
try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2009, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)
sbin_data_signal = pd.DataFrame(index=sbin_data.index)
sbin_data_signal['price'] = sbin_data['Close']
sbin_data_signal['daily_difference'] = sbin_data_signal['price'].diff()
sbin_data_signal['signal'] = 0.0
# Buy -> 1 and Sell -> 0
sbin_data_signal['signal'] = np.where(sbin_data_signal['daily_difference'] > 0, 1.0, 0.0)
# Long -> 1 and Short -> -1
sbin_data_signal['positions'] = sbin_data_signal['signal'].diff()

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI Price in Rs')
sbin_data_signal['price'].plot(ax=ax1, color='r', lw=2.)

ax1.plot(sbin_data_signal.loc[sbin_data_signal.positions == 1.0].index,
         sbin_data_signal.price[sbin_data_signal.positions == 1.0],
         '^', markersize=5, color='m')

ax1.plot(sbin_data_signal.loc[sbin_data_signal.positions == -1.0].index,
         sbin_data_signal.price[sbin_data_signal.positions == -1.0],
         'v', markersize=5, color='k')

# Set the initial capital
initial_capital = float(3000.0)
positions = pd.DataFrame(index=sbin_data_signal.index).fillna(0.0)
portfolio = pd.DataFrame(index=sbin_data_signal.index).fillna(0.0)
positions['SBIN'] = sbin_data_signal['signal']
portfolio['positions'] = (positions.multiply(sbin_data_signal['price'], axis=0))
portfolio['cash'] = initial_capital - (positions.diff().multiply(sbin_data_signal['price'], axis=0)).cumsum()
portfolio['total'] = portfolio['positions'] + portfolio['cash']
portfolio.plot()
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Portfolio value in Rs')
portfolio['total'].plot(ax=ax1, lw=2.)
ax1.plot(portfolio.loc[sbin_data_signal.positions == 1.0].index, portfolio.total[sbin_data_signal.positions == 1.0],
         '^', markersize=10, color='m')
ax1.plot(portfolio.loc[sbin_data_signal.positions == -1.0].index, portfolio.total[sbin_data_signal.positions == -1.0],
         'v', markersize=10, color='k')
plt.show()
