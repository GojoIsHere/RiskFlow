using System.ComponentModel.DataAnnotations;

namespace RiskFlow.Api.Models;

public record MarketRiskAnalysisRequest(
    string Asset,
    decimal Investment,
    string Period,
    double ConfidenceLevel,
    int TimeHorizonDays
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
        if (string.IsNullOrWhiteSpace(Asset))
        {
            yield return new ValidationResult(
                "Asset is required.",
                new[] { nameof(Asset) }
            );
        }

        if (Investment <= 0)
        {
            yield return new ValidationResult(
                "Investment must be greater than 0.",
                new[] { nameof(Investment) }
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
                "Time horizon must be greater than 0 days.",
                new[] { nameof(TimeHorizonDays) }
            );
        }
    }
}