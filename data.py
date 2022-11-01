import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from darts import TimeSeries
from darts.models import *
from darts.metrics import *
from darts.dataprocessing.transformers import Scaler
import logging

logging.disable(logging.CRITICAL)

### ---- Read data ----

df = pd.read_csv('data/monthly_in_situ_co2_mlo.csv',
                  comment = '"', header = [0,1,2], na_values = '-99.99')

cols = [' '.join(col).replace(' ', '') for col in df.columns.values]
df.set_axis(cols, axis = 1, inplace = True)

# Converting Excel date format to datetime and setting as dataframe index
df['datetime'] = pd.to_datetime(df['DateExcel'], origin = '1899-12-30', unit = 'D')
df.set_index('datetime', inplace = True)
df = df[['CO2filled[ppm]']]
df.rename(columns = {'CO2filled[ppm]': 'CO2'}, inplace = True)
df.dropna(inplace = True)
df = df.resample('M').sum()

#Loading the pandas dataframe to a TimeSeries object as required by the Darts library
series = TimeSeries.from_dataframe(df)
start = pd.Timestamp('123115')

df_metrics = pd.DataFrame()

def metrics(series, forecast, model_name):
    mae_ = mae(series, forecast)
    rmse_ = rmse(series, forecast)
    mape_ = mape(series, forecast)
    smape_ = smape(series, forecast)
    r2_score_ = r2_score(series, forecast)

    dict_ = {'MAE': mae_, 'RMSE': rmse_,
             'MAPE': mape_, 'SMAPE': smape_,
             'R2': r2_score_}

    df = pd.DataFrame(dict_, index = [model_name])

    return(df.round(decimals = 2))

### Create a naive forecasting model
model_naive = NaiveSeasonal(K = 12)
forecast_naive = model_naive.historical_forecasts(series, start=start, forecast_horizon=12, verbose=True)

### Create a Exponential Smoothing forecasting model
model_exp = ExponentialSmoothing(seasonal_periods = 12)
forecast_exp = model_exp.historical_forecasts(series, start=start, forecast_horizon=12, verbose=True)

### Create a Linear Regression forecasting model
model_reg = LinearRegressionModel(lags = 12)
forecast_reg = model_reg.historical_forecasts(series, start=start, forecast_horizon=12, verbose=True)
