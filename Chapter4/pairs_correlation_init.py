import pandas as pd
import numpy as np
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
import seaborn
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

tickers = ['ICICIBANK', 'HDFCBANK', 'HINDUNILVR', 'ITC']
tickers_data = []

for ticker in tickers:
    tickers_data.append(get_history(ticker, start=date(2004, 1, 1), end=date(2014, 1, 1)))


def find_cointegrated_pairs(data):
    n = len(data)
    pvalue_matrix = np.ones((n, n))
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            result = coint(data[i]['Close'], data[j]['Close'])
            pvalue_matrix[i, j] = result[1]
            if result[1] < 0.02:
                pairs.append((tickers[i], tickers[j]))
    return pvalue_matrix, pairs


pvalues, pairs = find_cointegrated_pairs(tickers_data)
print(pairs)
seaborn.heatmap(pvalues, xticklabels=tickers, yticklabels=tickers, cmap='RdYlGn_r', mask=(pvalues >= 0.98))
plt.show()
