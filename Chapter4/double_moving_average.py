import pandas as pd
import numpy as np
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt

SRC_DATA_FILENAME = '../sbin_data_large_chap4.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2001, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)


def double_moving_average(financial_data, short_window, long_window):
    signals = pd.DataFrame(index=financial_data.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = financial_data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = financial_data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
                                                > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['orders'] = signals['signal'].diff()
    return signals


ts = double_moving_average(sbin_data, 20, 100)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI Price in Rs')
sbin_data["Close"].plot(ax=ax1, color='g', lw=.5)
ts["short_mavg"].plot(ax=ax1, color='r', lw=2.)
ts["long_mavg"].plot(ax=ax1, color='b', lw=2.)
ax1.plot(ts.loc[ts.orders == 1.0].index, sbin_data["Close"][ts.orders == 1.0], '^', markersize=7, color='k')
ax1.plot(ts.loc[ts.orders == -1.0].index, sbin_data["Close"][ts.orders == -1.0], 'v', markersize=7, color='k')
plt.legend(["Price", "Short mavg", "Long mavg", "Buy", "Sell"])
plt.title("Double Moving Average Trading Strategy")

plt.show()
