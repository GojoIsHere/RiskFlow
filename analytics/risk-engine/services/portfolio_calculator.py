import numpy as np
import pandas as pd

from services.risk_calculator import (
    calculate_var,
    TRADING_DAYS_PER_YEAR
)


def calculate_portfolio_risk(
    prices: pd.DataFrame,
    investments: list[float],
    confidence_level: float,
    time_horizon_days: int
) -> dict:

    if len(prices.columns) != len(investments):
        raise ValueError(
            "Number of investments must match number of assets."
        )

    total_investment = sum(investments)

    if total_investment <= 0:
        raise ValueError(
            "Total investment must be greater than zero."
        )

    weights = np.array(investments) / total_investment

    daily_returns = prices.pct_change().dropna()

    mean_daily_returns = daily_returns.mean()

    covariance_matrix = daily_returns.cov()

    portfolio_daily_return = float(
        np.dot(weights, mean_daily_returns)
    )

    portfolio_daily_variance = float(
        np.dot(
            weights.T,
            np.dot(covariance_matrix, weights)
        )
    )

    portfolio_daily_volatility = float(
        np.sqrt(portfolio_daily_variance)
    )

    annualized_return = (
        portfolio_daily_return
        * TRADING_DAYS_PER_YEAR
    )

    annualized_volatility = (
        portfolio_daily_volatility
        * np.sqrt(TRADING_DAYS_PER_YEAR)
    )

    risk = calculate_var(
        investment=total_investment,
        expected_return=annualized_return,
        volatility=annualized_volatility,
        confidence_level=confidence_level,
        time_horizon_days=time_horizon_days
    )

    correlation_matrix = (
        daily_returns
        .corr()
        .round(4)
        .to_dict()
    )

    return {
        "totalInvestment": round(total_investment, 2),

        "portfolioMetrics": {
            "meanDailyReturn": round(
                portfolio_daily_return,
                6
            ),
            "dailyVolatility": round(
                portfolio_daily_volatility,
                6
            ),
            "annualizedReturn": round(
                annualized_return,
                6
            ),
            "annualizedVolatility": round(
                annualized_volatility,
                6
            )
        },

        "riskAnalysis": risk,

        "correlationMatrix": correlation_matrix
    }