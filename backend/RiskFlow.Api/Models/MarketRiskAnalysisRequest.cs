namespace RiskFlow.Api.Models;

public record MarketRiskAnalysisRequest(
    string Asset,
    decimal Investment,
    string Period,
    double ConfidenceLevel,
    int TimeHorizonDays
);