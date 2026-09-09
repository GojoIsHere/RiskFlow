using System.Net.Http.Json;
using RiskFlow.Api.Models;

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
}


public record RiskEngineHealth(
    string Service,
    string Status,
    string Version
);