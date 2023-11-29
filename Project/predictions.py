import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_next_year(df):

    predicted_df = pd.DataFrame(columns=df.columns)

    dfs = []
    for city in df.columns[:]:
        # Prepare the data for ARIMA

        data = df[[city]]

        data['d'] = data.index

        data.columns = ['y', 'd']

        # set the date colummn to date time
        data['Date'] = pd.to_datetime(data['d'])
        data.drop(columns=['d'], inplace=True)

        # Create and fit the ARIMA model
        model = ARIMA(data['y'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), freq='D')
        model_fit = model.fit()

        # get the last element of the data["Date"] column
        last_date = data['Date'].iloc[-1]

        # add one day to the last date
        last_date = last_date + pd.DateOffset(1) # type: ignore

        # Make future predictions for the next year
        future_dates = pd.date_range(start=last_date, periods=365, freq='D')
        forecast = model_fit.predict(start=len(data), end=len(data) + 364)

        # Create a dataframe for the predicted values
        predicted_values = pd.DataFrame({'Date': future_dates, city: forecast})

        
        # Append the predicted values to the output dataframe
        dfs.append(predicted_values.drop(columns=['Date']))

    predicted_df = pd.concat(dfs, axis=1)

    return predicted_df
