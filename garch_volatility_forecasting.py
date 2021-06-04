import numpy as np
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
from arch import arch_model
import statistics as stats
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_absolute_error, mean_squared_error
import math as math

data = get_history(symbol="NIFTY 50", start=date(2010, 1, 1), end=date(2021, 1, 1), index=True)
data.index = pd.to_datetime(data.index)
returns = 100 * data['Close'].pct_change().dropna()
# returns = 100 * np.log(data['Close']).diff().dropna()
lb_test_returns = acorr_ljungbox(returns, lags=5)
print("P-values for  Ljung-Box test on returns series are:\n")
print(*lb_test_returns, sep=',')

returns.plot(color='blue', lw=3., legend=True)
plt.legend(['Returns'], fontsize=16)
plt.show()

test_size = 250
returns_model_selection = returns[:-test_size]
plot_acf(returns_model_selection, title='Returns - ACF')
plot_pacf(returns_model_selection, title='Returns - PACF')
plot_acf(returns_model_selection**2, title='Returns*Returns - ACF')
plot_pacf(returns_model_selection**2, title='Returns*Returns - PACF')
plt.show()

model = arch_model(returns_model_selection, p=2, q=1)
model_fit = model.fit()
print(model_fit.summary())

rolling_predictions = []

time_period = 10  # look back period
history = []  # history of prices
sma_values = []  # to track moving average values for visualization purposes
stddev_values = []  # history of computed stdev values

for i in range(test_size):
    history.append(returns[-test_size + i])
    if len(history) > time_period:  # we track at most 'time_period' number of prices
        del (history[0])
    sma = stats.mean(history)
    sma_values.append(sma)
    variance = 0  # variance is square of standard deviation
    for hist_price in history:
        variance = variance + ((hist_price - sma) ** 2)
    stdev = math.sqrt(variance / len(history))
    stddev_values.append(stdev)
    train = returns[:-(test_size-i)]
    model = arch_model(train, p=2, q=1)
    model_fit = model.fit(disp='off')
    pred = model_fit.forecast(horizon=1, reindex=False)
    rolling_predictions.append(np.sqrt(pred.variance.values[-1][0]))

rolling_predictions = pd.Series(rolling_predictions, index=returns.index[-test_size:])
stddev_values = pd.Series(stddev_values, index=returns.index[-test_size:])
mae = mean_absolute_error(stddev_values, rolling_predictions)
mse = mean_squared_error(stddev_values, rolling_predictions)
print('MAE: ' + str(mae) + ' ' + 'MSE: ' + str(mse))

plt.figure(figsize=(10, 4))
plt.plot(returns[-test_size:])
plt.plot(rolling_predictions)
plt.plot(stddev_values)
plt.title('Volatility Prediction - Rolling Forecast', fontsize=20)
plt.legend(['True Returns', 'Predicted Volatility', 'Actual volatility'], fontsize=16)
plt.show()
