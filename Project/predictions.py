import pandas as pd
from sklearn.linear_model import LinearRegression

def create_lagged_features(df, lags):
    if df.empty:
        return df

    lagged_df = pd.DataFrame(index=df.index)

    for lag in lags:
        for col in df.columns:
            lagged_df[f'{col}_lag_{lag}'] = df[col].shift(lag)

    return lagged_df.dropna()

def predict_next_year(df, lags=3):
    predicted_df = pd.DataFrame(index=pd.date_range(start=df.index[-1] + pd.DateOffset(1), periods=365, freq='D'))

    for city in df.columns:
        # Prepare the data with lagged features
        lagged_df = create_lagged_features(df[[city]], range(1, lags + 1))
        
        if lagged_df.empty:
            # No lagged features available, cannot proceed with prediction
            continue

        # Split the data into features (X) and target (y)
        if city in lagged_df.columns:
            X = lagged_df.drop(city, axis=1)
            y = lagged_df[city]

            # Fit a linear regression model
            model = LinearRegression()
            model.fit(X, y)

            # Create lagged features for the next year
            future_dates = pd.date_range(start=predicted_df.index[0], periods=365, freq='D')
            future_lagged_df = create_lagged_features(pd.DataFrame(index=future_dates), range(1, lags + 1))

            # Make predictions for the next year
            if not future_lagged_df.empty:
                future_predictions = model.predict(future_lagged_df)
                # Create a DataFrame with predicted values
                predicted_values = pd.DataFrame(index=future_dates, data={city: future_predictions})
                # Append the predicted values to the output dataframe
                predicted_df = pd.concat([predicted_df, predicted_values], axis=1)
    
    print(predicted_df)
    return predicted_df
