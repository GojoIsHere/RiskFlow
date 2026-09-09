import numpy as np
import pandas as pd


def run_monte_carlo_simulation(
    prices: pd.DataFrame,
    investments: list[float],
    confidence_level: float,
    time_horizon_days: int,
    simulations: int = 10000,
    random_seed: int | None = None
) -> dict:

    if len(prices.columns) != len(investments):
        raise ValueError(
            "Number of investments must match number of assets."
        )

    if simulations < 1000 or simulations > 50000:
        raise ValueError(
            "Simulations must be between 1,000 and 50,000."
        )

    total_investment = sum(investments)

    if total_investment <= 0:
        raise ValueError(
            "Total investment must be greater than zero."
        )

    # Historical daily returns
    daily_returns = prices.pct_change().dropna()

    mean_returns = daily_returns.mean().to_numpy()

    covariance_matrix = (
        daily_returns.cov().to_numpy()
    )

    rng = np.random.default_rng(random_seed)

    # Shape:
    # simulations × days × assets
    simulated_returns = rng.multivariate_normal(
        mean=mean_returns,
        cov=covariance_matrix,
        size=(simulations, time_horizon_days)
    )

    # Compound each asset's simulated returns
    cumulative_returns = np.prod(
        1 + simulated_returns,
        axis=1
    )

    investments_array = np.array(
        investments,
        dtype=float
    )

    # Final simulated value for each portfolio path
    final_values = np.sum(
        investments_array * cumulative_returns,
        axis=1
    )

    profit_and_loss = (
        final_values - total_investment
    )

    losses = -profit_and_loss

    # Example:
    # 95% confidence → 95th percentile of losses
    value_at_risk = float(
        np.percentile(
            losses,
            confidence_level * 100
        )
    )

    value_at_risk = max(
        0.0,
        value_at_risk
    )

    tail_losses = losses[
        losses >= value_at_risk
    ]

    expected_shortfall = (
        float(tail_losses.mean())
        if len(tail_losses) > 0
        else value_at_risk
    )

    probability_of_loss = float(
        np.mean(profit_and_loss < 0)
    )

    return {
        "simulations": simulations,
        "expectedPortfolioValue": round(
            float(final_values.mean()),
            2
        ),
        "expectedProfitLoss": round(
            float(profit_and_loss.mean()),
            2
        ),
        "valueAtRisk": round(
            value_at_risk,
            2
        ),
        "expectedShortfall": round(
            max(0.0, expected_shortfall),
            2
        ),
        "probabilityOfLoss": round(
            probability_of_loss,
            4
        ),
        "bestSimulatedValue": round(
            float(final_values.max()),
            2
        ),
        "worstSimulatedValue": round(
            float(final_values.min()),
            2
        )
    }