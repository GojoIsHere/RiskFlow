namespace RiskFlow.Api.Models;

public record HistoricalRiskAnalysisRequest(
    string Asset,
    decimal Investment,
    List<double> Prices,
    double ConfidenceLevel,
    int TimeHorizonDays
);