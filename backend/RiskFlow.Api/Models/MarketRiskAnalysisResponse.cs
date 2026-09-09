namespace RiskFlow.Api.Models;

public record MarketRiskAnalysisResponse(
    string Asset,
    decimal Investment,
    string Period,
    int DataPoints,
    decimal LatestPrice,
    double ConfidenceLevel,
    int TimeHorizonDays,
    HistoricalMetricsData HistoricalMetrics,
    HistoricalRiskResult RiskAnalysis
);