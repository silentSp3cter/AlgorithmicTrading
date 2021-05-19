import pandas as pd
import matplotlib.pyplot as plt
from nsepy import get_history
from datetime import date
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot

SRC_DATA_FILENAME = '../sbin_data_large.pickle'

try:
    sbin_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    sbin_data = get_history('SBIN', start=date(2005, 1, 1), end=date(2013, 1, 1))
    sbin_data.to_pickle(SRC_DATA_FILENAME)
sbin_data.index = pd.to_datetime(sbin_data.index)
sbin_monthly_return = sbin_data['Close'].pct_change().groupby(
    [sbin_data['Close'].index.year,
     sbin_data['Close'].index.month]).mean()
sbin_monthly_return_list = []

for i in range(len(sbin_monthly_return)):
    sbin_monthly_return_list.append({'month': sbin_monthly_return.index[i][1],
                                     'monthly_return': sbin_monthly_return.iloc[i]})

sbin_monthly_return_list = pd.DataFrame(sbin_monthly_return_list, columns=('month', 'monthly_return'))

sbin_monthly_return_list.boxplot(column='monthly_return', by='month')
ax = plt.gca()
labels = [item.get_text() for item in ax.get_xticklabels()]
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', ' Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax.set_xticklabels(labels)
ax.set_ylabel('SBIN return')
plt.tick_params(axis='both', which='major', labelsize=7)
plt.title("SBIN Monthly return 2005-2012")
plt.suptitle("")
plt.show()

fig = plt.figure()
sbin_data['Close'].pct_change().groupby(
    [sbin_data['Close'].index.month])
ax1 = fig.add_subplot(111, ylabel='Monthly return')
sbin_monthly_return.plot()
plt.xlabel('Time')
plt.show()


# Displaying rolling statistics
def plot_rolling_statistics_ts(ts, titletext, ytext, window_size=12):
    plt.figure()
    ts.plot(color='red', label='Original', lw=0.5)
    ts.rolling(window_size).mean().plot(color='blue', label='Rolling Mean')
    ts.rolling(window_size).std().plot(color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.ylabel(ytext)
    plt.title(titletext)
    plt.show(block=False)


plot_rolling_statistics_ts(sbin_monthly_return[1:], 'SBIN prices rolling mean and standard deviation', 'Monthly return')
plot_rolling_statistics_ts(sbin_data['Close'], 'SBIN prices rolling mean and standard deviation',
                           'Daily prices', 365)
plot_rolling_statistics_ts(sbin_data['Close']-sbin_data['Close'].rolling(365).mean(),
                           'SBIN prices without trend', 'Daily prices', 365)


def test_stationarity(timeseries):
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries[1:], autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    print(dfoutput)


test_stationarity(sbin_monthly_return[1:])
test_stationarity(sbin_data['Close'])

pyplot.figure()
pyplot.subplot(211)
plot_acf(sbin_monthly_return[1:], ax=pyplot.gca(), lags=10)
pyplot.subplot(212)
plot_pacf(sbin_monthly_return[1:], ax=pyplot.gca(), lags=10)
pyplot.show()

model = ARIMA(sbin_monthly_return[1:], order=(2, 0, 2))
fitted_results = model.fit()
sbin_monthly_return[1:].plot()
fitted_results.fittedvalues.plot(color='red')
plt.show()
