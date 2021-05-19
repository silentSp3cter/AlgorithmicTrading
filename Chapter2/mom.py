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
The Momentum (MOM) indicator compares the current price with the previous price from a selected number of periods ago.
MOM =  Price - Price of n periods ago
'''
time_period = 20  # how far to look back to find reference price to compute momentum
history = []  # history of observed prices to use in momentum calculation
mom_values = []  # track momentum values for visualization purposes

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:  # history is at most 'time_period' number of observations
        del (history[0])
    mom = close_price - history[0]
    mom_values.append(mom)

sbin_data = sbin_data.assign(ClosePrice=pd.Series(close, index=sbin_data.index))
sbin_data = sbin_data.assign(MomentumFromPrice20DaysAgo=pd.Series(mom_values, index=sbin_data.index))

close_price = sbin_data['ClosePrice']
mom = sbin_data['MomentumFromPrice20DaysAgo']

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel='SBI price in Rs')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='Momentum in Rs')
mom.plot(ax=ax2, color='b', lw=2., legend=True)
plt.show()
