import pandas as pd
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt

SRC_DATA_FILENAME = '../sbin_data_large_chap4.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2001, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)


def turtle_trading(financial_data, window_size):
    signals = pd.DataFrame(index=financial_data.index)
    signals['orders'] = 0
    # window_size-days high
    signals['high'] = financial_data['Close'].shift(1).rolling(window=window_size).max()
    # window_size-days low
    signals['low'] = financial_data['Close'].shift(1).rolling(window=window_size).min()
    # window_size-days mean
    signals['avg'] = financial_data['Close'].shift(1).rolling(window=window_size).mean()
    # entry rule : stock price > the highest value for window_size day
    #              stock price < the lowest value for window_size day
    signals['long_entry'] = financial_data['Close'] > signals.high
    signals['short_entry'] = financial_data['Close'] < signals.low
    # exit rule : the stock price crosses the mean of past window_size days.
    signals['long_exit'] = financial_data['Close'] < signals.avg
    signals['short_exit'] = financial_data['Close'] > signals.avg
    position = 0
    for k in range(len(signals)):
        if signals['long_entry'][k] and position == 0:
            signals.orders.values[k] = 1
            position = 1
        elif signals['short_entry'][k] and position == 0:
            signals.orders.values[k] = -1
            position = -1
        elif signals['long_exit'][k] and position > 0:
            signals.orders.values[k] = -1
            position = 0
        elif signals['short_exit'][k] and position < 0:
            signals.orders.values[k] = 1
            position = 0
        else:
            signals.orders.values[k] = 0

    return signals


ts = turtle_trading(sbin_data, 50)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI price in Rs')
sbin_data["Close"].plot(ax=ax1, color='g', lw=.5)
ts["high"].plot(ax=ax1, color='black', lw=.5)
ts["low"].plot(ax=ax1, color='r', lw=.5)
ts["avg"].plot(ax=ax1, color='b', lw=.5)
ax1.plot(ts.loc[ts.orders == 1.0].index, sbin_data["Close"][ts.orders == 1.0], '^', markersize=7, color='k')
ax1.plot(ts.loc[ts.orders == -1.0].index, sbin_data["Close"][ts.orders == -1.0], 'v', markersize=7, color='k')
plt.legend(["Price", "Highs", "Lows", "Average", " Buy", " Sell"])
plt.title("Turtle Trading Strategy")

plt.show()
