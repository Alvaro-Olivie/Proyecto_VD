import pandas as pd
from statsmodels.tsa.ar_model import AutoReg

def predict_next_year(df):
    predicted_df = pd.DataFrame(index=pd.date_range(df.index[-1], periods=365, freq='D'))

    for city in df.columns:
        # Train an autoregressive model
        model = AutoReg(df[city], lags=3)
        model_fit = model.fit()

        # Make predictions for the next year
        predictions = model_fit.predict(start=len(df), end=len(df)+364)

        # Add the predictions to the output dataframe
        predicted_df[city] = predictions

    return predicted_df