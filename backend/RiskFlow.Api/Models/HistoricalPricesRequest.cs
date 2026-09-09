namespace RiskFlow.Api.Models;

public record HistoricalPricesRequest(
    List<double> Prices
);