namespace RiskFlow.Api.Models;

public record HistoricalRiskAnalysisResponse(
    string Asset,
    decimal Investment,
    double ConfidenceLevel,
    int TimeHorizonDays,
    HistoricalMetricsData HistoricalMetrics,
    HistoricalRiskResult RiskAnalysis
);

public record HistoricalRiskResult(
    decimal ValueAtRisk,
    decimal ExpectedGain,
    string RiskLevel
);