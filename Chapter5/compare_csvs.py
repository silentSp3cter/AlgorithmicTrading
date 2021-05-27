import pandas as pd
import matplotlib.pyplot as plt

basic_mr = pd.read_csv('basic_trend_following.csv')
vol_mr = pd.read_csv('volatility_adjusted_trend_following.csv')

basic_mr['Pnl'].plot(x='Date', color='b', lw=1., legend=True, label='Basic trend following strategy pnl')
vol_mr['Pnl'].plot(x='Date', color='g', lw=1., legend=True, label='Volatility adjusted trend following strategy pnl')
plt.show()
