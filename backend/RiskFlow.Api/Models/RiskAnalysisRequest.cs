namespace RiskFlow.Api.Models;

public record RiskAnalysisRequest(
    string Asset,
    decimal Investment,
    double ExpectedReturn,
    double Volatility,
    double ConfidenceLevel,
    int TimeHorizonDays
);