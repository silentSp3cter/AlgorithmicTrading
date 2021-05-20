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


def naive_momentum_trading(financial_data, nb_conseq_days):
    signals = pd.DataFrame(index=financial_data.index)
    signals['orders'] = 0
    cons_day = 0
    prior_price = 0
    init = True
    for k in range(len(financial_data['Close'])):
        price = financial_data['Close'][k]
        if init:
            prior_price = price
            init = False
        elif price > prior_price:
            if cons_day < 0:
                cons_day = 0
            cons_day += 1
        elif price < prior_price:
            if cons_day > 0:
                cons_day = 0
            cons_day -= 1
        if cons_day == nb_conseq_days:
            signals['orders'][k] = 1
        elif cons_day == -nb_conseq_days:
            signals['orders'][k] = -1

    return signals


ts = naive_momentum_trading(sbin_data, 5)
pd.set_option("display.max_rows", None, "display.max_columns", None)

print(sbin_data["Close"])

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='SBI price in Rs')
sbin_data["Close"].plot(ax=ax1, color='g', lw=.5)
ax1.plot(ts.loc[ts.orders == 1.0].index, sbin_data["Close"][ts.orders == 1], '^', markersize=7, color='k')
ax1.plot(ts.loc[ts.orders == -1.0].index, sbin_data["Close"][ts.orders == -1], 'v', markersize=7, color='k')
plt.legend(["Price", "Buy", "Sell"])
plt.title("Naive Momentum Trading Strategy")

plt.show()
