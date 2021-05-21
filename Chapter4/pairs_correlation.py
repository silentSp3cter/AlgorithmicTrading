import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

# Set a seed value to make the experience reproducible
np.random.seed(123)

# Generate Symbol1 daily returns
Symbol1_returns = np.random.normal(0, 1, 100)
# Create a series for Symbol1 prices
Symbol1_prices = pd.Series(np.cumsum(Symbol1_returns), name='Symbol1') + 10
# Create a series for Symbol2 prices
# We are going to mimic the Symbol1 behavior
noise = np.random.normal(0, 1, 100)
Symbol2_prices = Symbol1_prices + 10 + noise
Symbol2_prices.name = 'Symbol2'

plt.title("Symbol 1 and Symbol 2 prices")
Symbol1_prices.plot()
Symbol2_prices.plot()
plt.legend()
plt.show()


def zscore(series):
    return (series - series.mean()) / np.std(series)


score, pvalue, _ = coint(Symbol1_prices, Symbol2_prices)
print(pvalue)
ratios = Symbol1_prices / Symbol2_prices
plt.title("Ratios between Symbol 1 and Symbol 2 price")
ratios.plot()
plt.show()

zscore(ratios).plot()
plt.title("Z-score evolution")
plt.axhline(zscore(ratios).mean(),color="black")
plt.axhline(1.0, color="red")
plt.axhline(-1.0, color="green")
plt.show()

ratios.plot()
buy = ratios.copy()
sell = ratios.copy()
buy[zscore(ratios) > -1] = 0
sell[zscore(ratios) < 1] = 0
buy.plot(color="g", linestyle="None", marker="^")
sell.plot(color="r", linestyle="None", marker="v")
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, ratios.min(), ratios.max()))
plt.legend(["Ratio", "Buy Signal", "Sell Signal"])
plt.show()

symbol1_buy = Symbol1_prices.copy()
symbol1_sell = Symbol1_prices.copy()
symbol2_buy = Symbol2_prices.copy()
symbol2_sell = Symbol2_prices.copy()

Symbol1_prices.plot()
symbol1_buy[zscore(ratios) > -1] = 0
symbol1_sell[zscore(ratios) < 1] = 0
symbol1_buy.plot(color="g", linestyle="None", marker="^")
symbol1_sell.plot(color="r", linestyle="None", marker="v")

Symbol2_prices.plot()
symbol2_buy[zscore(ratios) < 1] = 0
symbol2_sell[zscore(ratios) > -1] = 0
symbol2_buy.plot(color="g", linestyle="None", marker="^")
symbol2_sell.plot(color="r", linestyle="None", marker="v")

x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, Symbol1_prices.min(), Symbol2_prices.max()))
plt.legend(["Symbol1", "Buy Signal", "Sell Signal", "Symbol2"])
plt.show()

pair_correlation_trading_strategy = pd.DataFrame(index=Symbol1_prices.index)
pair_correlation_trading_strategy['symbol1_price'] = Symbol1_prices
pair_correlation_trading_strategy['symbol1_buy'] = np.zeros(len(Symbol1_prices))
pair_correlation_trading_strategy['symbol1_sell'] = np.zeros(len(Symbol1_prices))
pair_correlation_trading_strategy['symbol2_buy'] = np.zeros(len(Symbol1_prices))
pair_correlation_trading_strategy['symbol2_sell'] = np.zeros(len(Symbol1_prices))

# Exit strategy when z-score is between -1 and +1
position = 0
for i in range(len(Symbol1_prices)):
    s1price = Symbol1_prices[i]
    s2price = Symbol2_prices[i]
    if not position and symbol1_buy[i] != 0:
        pair_correlation_trading_strategy['symbol1_buy'][i] = s1price
        pair_correlation_trading_strategy['symbol2_sell'][i] = s2price
        position = 1
    elif not position and symbol1_sell[i] != 0:
        pair_correlation_trading_strategy['symbol1_sell'][i] = s1price
        pair_correlation_trading_strategy['symbol2_buy'][i] = s2price
        position = -1
    elif position == -1 and (symbol1_sell[i] == 0 or i == len(Symbol1_prices)-1):
        pair_correlation_trading_strategy['symbol1_buy'][i] = s1price
        pair_correlation_trading_strategy['symbol2_sell'][i] = s2price
        position = 0
    elif position == 1 and (symbol1_buy[i] == 0 or i == len(Symbol1_prices)-1):
        pair_correlation_trading_strategy['symbol1_sell'][i] = s1price
        pair_correlation_trading_strategy['symbol2_buy'][i] = s2price
        position = 0

# calculating strategy P & L
pair_correlation_trading_strategy['symbol1_position'] = pair_correlation_trading_strategy['symbol1_sell'] - \
                                                        pair_correlation_trading_strategy['symbol1_buy']

pair_correlation_trading_strategy['symbol2_position'] = pair_correlation_trading_strategy['symbol2_sell'] -\
                                                        pair_correlation_trading_strategy['symbol2_buy']

pair_correlation_trading_strategy['symbol1_position'].cumsum().plot()
pair_correlation_trading_strategy['symbol2_position'].cumsum().plot()

pair_correlation_trading_strategy['total_position'] = pair_correlation_trading_strategy['symbol1_position'] + \
                                                      pair_correlation_trading_strategy['symbol2_position']
pair_correlation_trading_strategy['total_position'].cumsum().plot()
plt.title("Symbol 1 and Symbol 2 positions")
plt.legend()
plt.show()
