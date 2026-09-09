namespace RiskFlow.Api.Models;

public record RiskAnalysisResponse(
    string Asset,
    decimal Investment,
    double ExpectedReturn,
    double Volatility,
    double ConfidenceLevel,
    int TimeHorizonDays,
    decimal ValueAtRisk,
    decimal ExpectedGain,
    string RiskLevel
);