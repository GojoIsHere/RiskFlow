namespace RiskFlow.Api.Models;

public record MonteCarloPortfolioResponse(
    List<string> Portfolio,
    decimal TotalInvestment,
    string Period,
    int DataPoints,
    double ConfidenceLevel,
    int TimeHorizonDays,
    MonteCarloSimulation Simulation
);

public record MonteCarloSimulation(
    int Simulations,
    decimal ExpectedPortfolioValue,
    decimal ExpectedProfitLoss,
    decimal ValueAtRisk,
    decimal ExpectedShortfall,
    double ProbabilityOfLoss,
    decimal BestSimulatedValue,
    decimal WorstSimulatedValue
);