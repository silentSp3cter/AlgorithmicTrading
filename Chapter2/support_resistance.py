import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nsepy import get_history
from datetime import date

SRC_DATA_FILENAME = '../sbin_data.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2009, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)

sbin_data_signal = pd.DataFrame(index=sbin_data.index)
sbin_data_signal['price'] = sbin_data['Close']


def trading_support_resistance(data, bin_width=20):
    data['sup_tolerance'] = pd.Series(np.zeros(len(data)))
    data['res_tolerance'] = pd.Series(np.zeros(len(data)))
    data['sup_count'] = pd.Series(np.zeros(len(data)))
    data['res_count'] = pd.Series(np.zeros(len(data)))
    data['sup'] = pd.Series(np.zeros(len(data)))
    data['res'] = pd.Series(np.zeros(len(data)))
    data['positions'] = pd.Series(np.zeros(len(data)))
    data['signal'] = pd.Series(np.zeros(len(data)))
    in_support = 0
    in_resistance = 0
    for x in range((bin_width - 1) + bin_width, len(data)):
        data_section = data[x - bin_width: x + 1]
        support_level = min(data_section['price'])
        resistance_level = max(data_section['price'])
        range_level = resistance_level - support_level
        data['res'][x] = resistance_level
        data['sup'][x] = support_level
        data['sup_tolerance'][x] = support_level + 0.2 * range_level
        data['res_tolerance'][x] = resistance_level - 0.2 * range_level
        if data['res_tolerance'][x] <= data['price'][x] <= data['res'][x]:
            in_resistance += 1
            data['res_count'][x] = in_resistance
        elif data['sup'][x] <= data['price'][x] <= data['sup_tolerance'][x]:
            in_support += 1
            data['sup_count'][x] = in_support
        else:
            in_support = 0
            in_resistance = 0
        if in_resistance > 2:
            data['signal'][x] = 1  # Buy signal
        elif in_support > 2:
            data['signal'][x] = 0  # Sell signal
        else:
            data['signal'][x] = data['signal'][x-1]
    data['positions'] = data['signal'].diff()  # 1 -> Long & -1 -> Short


trading_support_resistance(sbin_data_signal)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI price in Rs')
sbin_data_signal['sup'].plot(ax=ax1, color='g', lw=2.)
sbin_data_signal['res'].plot(ax=ax1, color='b', lw=2.)
sbin_data_signal['price'].plot(ax=ax1, color='r', lw=2.)
ax1.plot(sbin_data_signal.loc[sbin_data_signal.positions == 1.0].index,
         sbin_data_signal.price[sbin_data_signal.positions == 1.0], '^', markersize=7, color='k', label='buy')
ax1.plot(sbin_data_signal.loc[sbin_data_signal.positions == -1.0].index,
         sbin_data_signal.price[sbin_data_signal.positions == -1.0], 'v', markersize=7, color='k', label='sell')
plt.legend()
plt.show()
