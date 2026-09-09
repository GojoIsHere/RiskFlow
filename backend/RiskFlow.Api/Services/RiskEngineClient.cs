using System.Net.Http.Json;
using RiskFlow.Api.Models;
using RiskFlow.Api.Exceptions;
using System.Text.Json;

namespace RiskFlow.Api.Services;

public class RiskEngineClient
{
    private readonly HttpClient _httpClient;

    public RiskEngineClient(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<RiskEngineHealth?> GetHealthAsync()
    {
        return await _httpClient
            .GetFromJsonAsync<RiskEngineHealth>("/health");
    }

    public async Task<RiskAnalysisResponse?> AnalyzeRiskAsync(
        RiskAnalysisRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "/analyze",
            request
        );

        response.EnsureSuccessStatusCode();

        return await response.Content
            .ReadFromJsonAsync<RiskAnalysisResponse>();
    }

    public async Task<HistoricalMetricsResponse?> GetHistoricalMetricsAsync(
        HistoricalPricesRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "/historical-metrics",
            request
        );

        response.EnsureSuccessStatusCode();

        return await response.Content
            .ReadFromJsonAsync<HistoricalMetricsResponse>();
    }
    public async Task<HistoricalRiskAnalysisResponse?> AnalyzeHistoryAsync(
    HistoricalRiskAnalysisRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "/analyze-history",
            request
        );

        response.EnsureSuccessStatusCode();

        return await response.Content
            .ReadFromJsonAsync<HistoricalRiskAnalysisResponse>();
    }

    public async Task<MarketRiskAnalysisResponse?> AnalyzeMarketAsync(
    MarketRiskAnalysisRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "/analyze-market",
            request
        );

        if (!response.IsSuccessStatusCode)
        {
            var message =
                await ReadErrorMessageAsync(response);

            throw new RiskEngineException(
                (int)response.StatusCode,
                message
            );
        }

        return await response.Content
            .ReadFromJsonAsync<MarketRiskAnalysisResponse>();
    }

    private static async Task<string> ReadErrorMessageAsync(
    HttpResponseMessage response)
    {
        var content = await response.Content.ReadAsStringAsync();

        if (string.IsNullOrWhiteSpace(content))
        {
            return "Risk engine request failed.";
        }

        try
        {
            using var document = JsonDocument.Parse(content);

            if (document.RootElement.TryGetProperty(
                "detail",
                out var detail))
            {
                if (detail.ValueKind == JsonValueKind.String)
                {
                    return detail.GetString()
                        ?? "Risk engine request failed.";
                }

                return detail.ToString();
            }
        }
        catch (JsonException)
        {
            // Fall back to the original response body.
        }

        return content;
    }
}


public record RiskEngineHealth(
    string Service,
    string Status,
    string Version
);