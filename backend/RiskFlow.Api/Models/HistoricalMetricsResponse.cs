namespace RiskFlow.Api.Models;

public record HistoricalMetricsResponse(
    string Status,
    HistoricalMetricsData Data
);

public record HistoricalMetricsData(
    double MeanDailyReturn,
    double DailyVolatility,
    double AnnualizedReturn,
    double AnnualizedVolatility
);