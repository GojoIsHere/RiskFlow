using System.ComponentModel.DataAnnotations;

namespace RiskFlow.Api.Models;

public record MonteCarloPortfolioRequest(
    List<PortfolioAssetRequest> Assets,
    string Period,
    double ConfidenceLevel,
    int TimeHorizonDays,
    int Simulations = 10000,
    int? RandomSeed = null
) : IValidatableObject
{
    private static readonly HashSet<string> SupportedPeriods =
        new(StringComparer.OrdinalIgnoreCase)
        {
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y"
        };

    public IEnumerable<ValidationResult> Validate(
        ValidationContext validationContext)
    {
        if (Assets is null || Assets.Count < 2)
        {
            yield return new ValidationResult(
                "Portfolio must contain at least two assets.",
                new[] { nameof(Assets) }
            );

            yield break;
        }

        foreach (var asset in Assets)
        {
            if (string.IsNullOrWhiteSpace(asset.Symbol))
            {
                yield return new ValidationResult(
                    "Every asset must have a symbol.",
                    new[] { nameof(Assets) }
                );
            }

            if (asset.Investment <= 0)
            {
                yield return new ValidationResult(
                    $"Investment for {asset.Symbol} must be greater than 0.",
                    new[] { nameof(Assets) }
                );
            }
        }

        var symbols = Assets
            .Select(asset => asset.Symbol.Trim().ToUpperInvariant())
            .ToList();

        if (symbols.Count != symbols.Distinct().Count())
        {
            yield return new ValidationResult(
                "Portfolio cannot contain duplicate assets.",
                new[] { nameof(Assets) }
            );
        }

        if (string.IsNullOrWhiteSpace(Period) ||
            !SupportedPeriods.Contains(Period))
        {
            yield return new ValidationResult(
                "Period must be one of: 1mo, 3mo, 6mo, 1y, 2y, 5y.",
                new[] { nameof(Period) }
            );
        }

        if (ConfidenceLevel <= 0.5 ||
            ConfidenceLevel >= 1)
        {
            yield return new ValidationResult(
                "Confidence level must be greater than 0.5 and less than 1.",
                new[] { nameof(ConfidenceLevel) }
            );
        }

        if (TimeHorizonDays <= 0)
        {
            yield return new ValidationResult(
                "Time horizon must be greater than 0.",
                new[] { nameof(TimeHorizonDays) }
            );
        }

        if (Simulations < 1000 || Simulations > 50000)
        {
            yield return new ValidationResult(
                "Simulations must be between 1,000 and 50,000.",
                new[] { nameof(Simulations) }
            );
        }
    }
}