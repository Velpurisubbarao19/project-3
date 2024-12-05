# -*- coding: utf-8 -*-
"""Monthly (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12N0obX6BY8dgHeAFlxWe6op1RU-_Hb7f
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

# Load and preprocess the datamonthly_d
monthly_data = pd.read_csv(r"C:\Users\91970\Downloads\SN_m_tot_V2.0.csv", delimiter=';', header=None)
monthly_data.columns = ["Year", "Month", "FractionalYear", "MonthlyMeanSunspotNumber", "StdDev", "Observations", "Indicator"]
monthly_data = monthly_data[monthly_data["MonthlyMeanSunspotNumber"] != -1]  # Remove missing values

# Create a datetime column
monthly_data['Date'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(Day=1))
monthly_data = monthly_data[['Date', "MonthlyMeanSunspotNumber"]].rename(columns={'Date': 'ds', "MonthlyMeanSunspotNumber": 'y'})

# Replace zero values and apply log transformation
monthly_data['y'] = monthly_data['y'].replace(0, 1e-6)
monthly_data['y'] = monthly_data['y'].apply(lambda x: np.log(x + 1e-6))
monthly_data = monthly_data[monthly_data['y'] > 0]  # Keep only positive values

# Initialize and fit the Prophet model
monthly_model = Prophet()
monthly_model.fit(monthly_data)

# Create future dataframes for predictions
future_monthly = monthly_model.make_future_dataframe(periods=9, freq='M')

# Predict for the next 1, 6, and 9 months
forecasts = {
    "1 Month": monthly_model.predict(monthly_model.make_future_dataframe(periods=1, freq='M')),
    "6 Months": monthly_model.predict(monthly_model.make_future_dataframe(periods=6, freq='M')),
    "9 Months": monthly_model.predict(monthly_model.make_future_dataframe(periods=9, freq='M'))
}

# Visualize predictions for each forecast
for period, forecast in forecasts.items():
    fig = monthly_model.plot(forecast)
    plt.title(f"Sunspot Forecast: Next {period}")
    plt.show()
    print(f"Predicted values for the next {period}:")
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast.shape[0]))

# Final visualization of the monthly forecast
fig_final = monthly_model.plot(monthly_model.predict(future_monthly))
plt.title("Monthly Sunspot Forecasting")
plt.xlabel("Date")
plt.ylabel("Sunspot Number")
plt.show()

# Fit the model with additional seasonality
monthly_model = Prophet(growth='linear', changepoint_prior_scale=0.05)
monthly_model.add_seasonality(name='yearly', period=12, fourier_order=10)

# Fit and predict again
monthly_model.fit(monthly_data)
forecast_monthly = monthly_model.predict(future_monthly)

# Calculate metrics for the last 9 months
y_true = monthly_data['y'].tail(9)
y_pred = forecast_monthly['yhat'][-9:]

mae = mean_absolute_error(y_true, y_pred)
mape = mean_absolute_percentage_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print(f"Metrics for the last 9 months: MAE: {mae}, MAPE: {mape}, R²: {r2}")


