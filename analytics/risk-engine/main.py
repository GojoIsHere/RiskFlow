from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from math import sqrt
from statistics import NormalDist
from services.risk_calculator import (
    calculate_returns,
    calculate_var
)
from services.market_data import (
    get_historical_prices,
    get_portfolio_price_history
)
from services.portfolio_calculator import (
    calculate_portfolio_risk
)

app = FastAPI(
    title="RiskFlow Risk Engine",
    description="Python analytics service for RiskFlow.",
    version="0.1.0",
)


class RiskAnalysisRequest(BaseModel):
    asset: str
    investment: float = Field(gt=0)
    expectedReturn: float
    volatility: float = Field(gt=0)
    confidenceLevel: float = Field(gt=0.5, lt=1)
    timeHorizonDays: int = Field(gt=0)


class HistoricalPricesRequest(BaseModel):
    prices: list[float]


class RiskAnalysisResponse(BaseModel):
    asset: str
    investment: float
    expectedReturn: float
    volatility: float
    confidenceLevel: float
    timeHorizonDays: int
    valueAtRisk: float
    expectedGain: float
    riskLevel: str


class HistoricalRiskAnalysisRequest(BaseModel):
    asset: str
    investment: float = Field(gt=0)
    prices: list[float]
    confidenceLevel: float = Field(gt=0.5, lt=1)
    timeHorizonDays: int = Field(gt=0)



SUPPORTED_PERIODS = {
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y"
}


class MarketRiskAnalysisRequest(BaseModel):
    asset: str
    investment: float = Field(gt=0)
    period: str = "1y"
    confidenceLevel: float = Field(gt=0.5, lt=1)
    timeHorizonDays: int = Field(gt=0)

    @field_validator("asset")
    @classmethod
    def validate_asset(cls, value: str) -> str:
        value = value.strip().upper()

        if not value:
            raise ValueError("Asset is required.")

        return value

    @field_validator("period")
    @classmethod
    def validate_period(cls, value: str) -> str:
        value = value.strip().lower()

        if value not in SUPPORTED_PERIODS:
            raise ValueError(
                "Period must be one of: "
                "1mo, 3mo, 6mo, 1y, 2y, 5y."
            )

        return value

class PortfolioAsset(BaseModel):
    symbol: str
    investment: float = Field(gt=0)

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, value: str) -> str:
        value = value.strip().upper()

        if not value:
            raise ValueError("Symbol is required.")

        return value


class PortfolioRiskRequest(BaseModel):
    assets: list[PortfolioAsset]
    period: str = "1y"
    confidenceLevel: float = Field(gt=0.5, lt=1)
    timeHorizonDays: int = Field(gt=0)

    @field_validator("assets")
    @classmethod
    def validate_assets(
        cls,
        value: list[PortfolioAsset]
    ) -> list[PortfolioAsset]:

        if len(value) < 2:
            raise ValueError(
                "Portfolio must contain at least two assets."
            )

        symbols = [
            asset.symbol
            for asset in value
        ]

        if len(symbols) != len(set(symbols)):
            raise ValueError(
                "Portfolio cannot contain duplicate assets."
            )

        return value

    @field_validator("period")
    @classmethod
    def validate_period(cls, value: str) -> str:
        value = value.strip().lower()

        if value not in SUPPORTED_PERIODS:
            raise ValueError(
                "Period must be one of: "
                "1mo, 3mo, 6mo, 1y, 2y, 5y."
            )

        return value

@app.get("/")
def root():
    return {
        "service": "RiskFlow Risk Engine",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "service": "risk-engine",
        "status": "healthy",
        "version": "0.1.0"
    }


@app.post("/historical-metrics")
def historical_metrics(request: HistoricalPricesRequest):
    try:
        metrics = calculate_returns(request.prices)

        return {
            "status": "success",
            "data": metrics
        }

    except ValueError as error:
        return {
            "status": "error",
            "message": str(error)
        }

@app.post("/analyze", response_model=RiskAnalysisResponse)
def analyze_risk(request: RiskAnalysisRequest):

    trading_days_per_year = 252

    time_fraction = request.timeHorizonDays / trading_days_per_year

    z_score = NormalDist().inv_cdf(request.confidenceLevel)

    expected_gain = (
        request.investment
        * request.expectedReturn
        * time_fraction
    )

    volatility_loss = (
        request.investment
        * z_score
        * request.volatility
        * sqrt(time_fraction)
    )

    value_at_risk = max(
        0,
        volatility_loss - expected_gain
    )

    var_percentage = (
        value_at_risk / request.investment
    ) * 100

    if var_percentage < 2:
        risk_level = "Low"
    elif var_percentage < 5:
        risk_level = "Moderate"
    elif var_percentage < 10:
        risk_level = "High"
    else:
        risk_level = "Very High"

    return RiskAnalysisResponse(
        asset=request.asset,
        investment=round(request.investment, 2),
        expectedReturn=request.expectedReturn,
        volatility=request.volatility,
        confidenceLevel=request.confidenceLevel,
        timeHorizonDays=request.timeHorizonDays,
        valueAtRisk=round(value_at_risk, 2),
        expectedGain=round(expected_gain, 2),
        riskLevel=risk_level
    )


@app.post("/analyze-history")
def analyze_history(
    request: HistoricalRiskAnalysisRequest
):
    metrics = calculate_returns(request.prices)

    risk = calculate_var(
        investment=request.investment,
        expected_return=metrics["annualizedReturn"],
        volatility=metrics["annualizedVolatility"],
        confidence_level=request.confidenceLevel,
        time_horizon_days=request.timeHorizonDays
    )

    return {
        "asset": request.asset,
        "investment": request.investment,
        "confidenceLevel": request.confidenceLevel,
        "timeHorizonDays": request.timeHorizonDays,
        "historicalMetrics": metrics,
        "riskAnalysis": risk
    }


@app.post("/analyze-market")
def analyze_market(
    request: MarketRiskAnalysisRequest
):
    try:
        prices = get_historical_prices(
            symbol=request.asset,
            period=request.period
        )

        metrics = calculate_returns(prices)

        risk = calculate_var(
            investment=request.investment,
            expected_return=metrics["annualizedReturn"],
            volatility=metrics["annualizedVolatility"],
            confidence_level=request.confidenceLevel,
            time_horizon_days=request.timeHorizonDays
        )

        return {
            "asset": request.asset.upper(),
            "investment": request.investment,
            "period": request.period,
            "dataPoints": len(prices),
            "latestPrice": round(prices[-1], 2),
            "confidenceLevel": request.confidenceLevel,
            "timeHorizonDays": request.timeHorizonDays,
            "historicalMetrics": metrics,
            "riskAnalysis": risk
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@app.post("/analyze-portfolio")
def analyze_portfolio(
    request: PortfolioRiskRequest
):
    try:
        symbols = [
            asset.symbol
            for asset in request.assets
        ]

        investments = [
            asset.investment
            for asset in request.assets
        ]

        prices = get_portfolio_price_history(
            symbols=symbols,
            period=request.period
        )

        analysis = calculate_portfolio_risk(
            prices=prices,
            investments=investments,
            confidence_level=request.confidenceLevel,
            time_horizon_days=request.timeHorizonDays
        )

        holdings = []

        total_investment = sum(investments)

        for asset in request.assets:
            holdings.append({
                "symbol": asset.symbol,
                "investment": asset.investment,
                "weight": round(
                    asset.investment / total_investment,
                    4
                ),
                "latestPrice": round(
                    float(prices[asset.symbol].iloc[-1]),
                    2
                )
            })

        return {
            "period": request.period,
            "dataPoints": len(prices),
            "confidenceLevel": request.confidenceLevel,
            "timeHorizonDays": request.timeHorizonDays,
            "holdings": holdings,
            **analysis
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )