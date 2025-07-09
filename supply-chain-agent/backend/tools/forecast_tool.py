from ibm_watsonx_orchestrate.agent_builder.tools import tool
from prophet import Prophet
import pandas as pd

@tool
def generate_sales_forecast(freq: str = 'W', periods: int = 4) -> list:
    """
    Forecast sales using hardcoded data and return predictions.

    Parameters:
    - freq: Frequency of forecast ('W' for weekly)
    - periods: Number of periods to forecast

    Returns:
    - A list of dictionaries with forecast results:
      - 'date'
      - 'predicted_sales'
      - 'lower_bound'
      - 'upper_bound'
    """
    # Hardcoded historical sales data
    data = pd.DataFrame({
        "ds": pd.date_range(start="2025-01-01", periods=10, freq="W"),
        "y": [180, 190, 200, 210, 205, 215, 220, 225, 230, 235]
    })

    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    result = forecast.tail(periods)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    return [
        {
            "date": row["ds"].strftime("%Y-%m-%d"),
            "predicted_sales": round(row["yhat"], 2),
            "lower_bound": round(row["yhat_lower"], 2),
            "upper_bound": round(row["yhat_upper"], 2),
        }
        for _, row in result.iterrows()
    ]
