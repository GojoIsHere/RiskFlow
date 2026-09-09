import yfinance as yf
import pandas as pd


def get_historical_prices(
    symbol: str,
    period: str = "1y"
) -> list[float]:

    ticker = yf.Ticker(symbol)

    history = ticker.history(
        period=period,
        interval="1d",
        auto_adjust=True
    )

    if history.empty:
        raise ValueError(
            f"No historical market data found for '{symbol}'."
        )

    prices = (
        history["Close"]
        .dropna()
        .astype(float)
        .tolist()
    )

    if len(prices) < 2:
        raise ValueError(
            f"Not enough historical prices available for '{symbol}'."
        )

    return prices


def get_portfolio_price_history(
    symbols: list[str],
    period: str = "1y"
) -> pd.DataFrame:

    price_data = {}

    for symbol in symbols:
        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period=period,
            interval="1d",
            auto_adjust=True
        )

        if history.empty:
            raise ValueError(
                f"No historical market data found for '{symbol}'."
            )

        close_prices = history["Close"].dropna()

        if len(close_prices) < 2:
            raise ValueError(
                f"Not enough historical prices available for '{symbol}'."
            )

        price_data[symbol] = close_prices

    prices = pd.DataFrame(price_data)

    # Keep only dates where all assets have prices
    prices = prices.dropna()

    if len(prices) < 2:
        raise ValueError(
            "Not enough overlapping market data for the portfolio."
        )

    return prices