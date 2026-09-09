namespace RiskFlow.Api.Models;

public record PortfolioRiskResponse(
    string Period,
    int DataPoints,
    double ConfidenceLevel,
    int TimeHorizonDays,
    List<PortfolioHolding> Holdings,
    decimal TotalInvestment,
    PortfolioMetrics PortfolioMetrics,
    HistoricalRiskResult RiskAnalysis,
    Dictionary<string, Dictionary<string, double>> CorrelationMatrix
);

public record PortfolioHolding(
    string Symbol,
    decimal Investment,
    double Weight,
    decimal LatestPrice
);

public record PortfolioMetrics(
    double MeanDailyReturn,
    double DailyVolatility,
    double AnnualizedReturn,
    double AnnualizedVolatility
);