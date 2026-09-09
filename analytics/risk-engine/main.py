from fastapi import FastAPI
from pydantic import BaseModel, Field
from math import sqrt
from statistics import NormalDist
from services.risk_calculator import calculate_returns

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