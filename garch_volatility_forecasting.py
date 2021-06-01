import numpy as np
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
from arch import arch_model

data = get_history(symbol="NIFTY 50", start=date(2010, 1, 1), end=date(2021, 1, 1), index=True)
data.index = pd.to_datetime(data.index)
returns = 100 * data['Close'].pct_change().dropna()
returns.plot(color='blue', lw=3., legend=True)
plt.legend(['Returns'], fontsize=16)
plt.show()

rolling_predictions = []
test_size = 250

for i in range(test_size):
    train = returns[:-(test_size-i)]
    model = arch_model(train, p=2, q=2)
    model_fit = model.fit(disp='off')
    pred = model_fit.forecast(horizon=1, reindex=False)
    rolling_predictions.append(np.sqrt(pred.variance.values[-1][0]))

rolling_predictions = pd.Series(rolling_predictions, index=returns.index[-test_size:])

plt.figure(figsize=(10, 4))
true, = plt.plot(returns[-test_size:])
preds, = plt.plot(rolling_predictions)
plt.title('Volatility Prediction - Rolling Forecast', fontsize=20)
plt.legend(['True Returns', 'Predicted Volatility'], fontsize=16)
plt.show()

train = returns[:-7]
model = arch_model(train, p=2, q=2)
model_fit = model.fit(disp='off')

pred = model_fit.forecast(horizon=7, reindex=False)
future_dates = returns.index[-7:]
pred = pd.Series(np.sqrt(pred.variance.values[-1, :]), index=future_dates)

plt.figure(figsize=(10, 4))
plt.plot(returns.index[-7:], returns[-7:], color='blue', lw=2.)
plt.plot(pred.index, pred, color='black', lw=2.)
plt.legend(['True Returns', 'Predicted Volatility'], fontsize=16)
plt.title('Volatility Prediction - Next 7 Days', fontsize=20)
plt.show()
