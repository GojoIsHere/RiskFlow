import numpy as np
import pandas as pd

from math import sqrt
from statistics import NormalDist


TRADING_DAYS_PER_YEAR = 252


def calculate_returns(prices: list[float]) -> dict:
    if len(prices) < 2:
        raise ValueError("At least two prices are required.")

    price_series = pd.Series(prices)

    daily_returns = price_series.pct_change().dropna()

    mean_daily_return = daily_returns.mean()
    daily_volatility = daily_returns.std()

    annualized_return = mean_daily_return * TRADING_DAYS_PER_YEAR

    annualized_volatility = (
        daily_volatility * np.sqrt(TRADING_DAYS_PER_YEAR)
    )

    return {
        "meanDailyReturn": round(float(mean_daily_return), 6),
        "dailyVolatility": round(float(daily_volatility), 6),
        "annualizedReturn": round(float(annualized_return), 6),
        "annualizedVolatility": round(float(annualized_volatility), 6),
    }


def calculate_var(
    investment: float,
    expected_return: float,
    volatility: float,
    confidence_level: float,
    time_horizon_days: int
) -> dict:

    time_fraction = (
        time_horizon_days / TRADING_DAYS_PER_YEAR
    )

    z_score = NormalDist().inv_cdf(confidence_level)

    expected_gain = (
        investment
        * expected_return
        * time_fraction
    )

    volatility_loss = (
        investment
        * z_score
        * volatility
        * sqrt(time_fraction)
    )

    value_at_risk = max(
        0,
        volatility_loss - expected_gain
    )

    var_percentage = (
        value_at_risk / investment
    ) * 100

    if var_percentage < 2:
        risk_level = "Low"
    elif var_percentage < 5:
        risk_level = "Moderate"
    elif var_percentage < 10:
        risk_level = "High"
    else:
        risk_level = "Very High"

    return {
        "valueAtRisk": round(value_at_risk, 2),
        "expectedGain": round(expected_gain, 2),
        "riskLevel": risk_level
    }