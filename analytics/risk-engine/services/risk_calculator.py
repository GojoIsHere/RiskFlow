import numpy as np
import pandas as pd


def calculate_returns(prices: list[float]) -> dict:
    if len(prices) < 2:
        raise ValueError("At least two prices are required.")

    price_series = pd.Series(prices)

    daily_returns = price_series.pct_change().dropna()

    mean_daily_return = daily_returns.mean()
    daily_volatility = daily_returns.std()

    annualized_return = mean_daily_return * 252
    annualized_volatility = daily_volatility * np.sqrt(252)

    return {
        "meanDailyReturn": round(float(mean_daily_return), 6),
        "dailyVolatility": round(float(daily_volatility), 6),
        "annualizedReturn": round(float(annualized_return), 6),
        "annualizedVolatility": round(float(annualized_volatility), 6),
    }