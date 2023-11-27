import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_next_year(df):
    predicted_df = pd.DataFrame(columns=df.columns)

    for city in df.columns[1:]:
        # Prepare the data for ARIMA
        data = df[['Date', city]].rename(columns={'Date': 'ds', city: 'y'})
        data['ds'] = pd.to_datetime(data['ds'])

        # Create and fit the ARIMA model
        model = ARIMA(data['y'], order=(1, 1, 1))
        model_fit = model.fit()

        # Make future predictions for the next year
        future_dates = pd.date_range(start=data['ds'].iloc[-1], periods=365, freq='D')
        forecast = model_fit.predict(start=len(data), end=len(data) + 364)

        # Create a dataframe for the predicted values
        predicted_values = pd.DataFrame({'Date': future_dates, city: forecast})

        # Append the predicted values to the output dataframe
        predicted_df = pd.concat([predicted_df, predicted_values], ignore_index=True)

    return predicted_df
