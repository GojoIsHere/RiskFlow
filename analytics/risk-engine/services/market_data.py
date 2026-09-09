import yfinance as yf


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