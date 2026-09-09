using Microsoft.AspNetCore.Mvc;
using RiskFlow.Api.Models;
using RiskFlow.Api.Services;

namespace RiskFlow.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class RiskController : ControllerBase
{
    private readonly RiskEngineClient _riskEngineClient;

    public RiskController(RiskEngineClient riskEngineClient)
    {
        _riskEngineClient = riskEngineClient;
    }

    [HttpGet("health")]
    public async Task<IActionResult> GetHealth()
    {
        var riskEngineHealth =
            await _riskEngineClient.GetHealthAsync();

        return Ok(new
        {
            service = "RiskFlow API",
            status = "healthy",
            riskEngine = riskEngineHealth
        });
    }

    [HttpPost("analyze")]
    public async Task<IActionResult> AnalyzeRisk(
        [FromBody] RiskAnalysisRequest request)
    {
        var result =
            await _riskEngineClient.AnalyzeRiskAsync(request);

        return Ok(new
        {
            service = "RiskFlow API",
            analysis = result
        });
    }

    [HttpPost("historical-metrics")]
    public async Task<IActionResult> GetHistoricalMetrics(
        [FromBody] HistoricalPricesRequest request)
    {
        var result =
            await _riskEngineClient.GetHistoricalMetricsAsync(request);

        return Ok(new
        {
            service = "RiskFlow API",
            metrics = result
        });
    }

    [HttpPost("analyze-history")]
    public async Task<IActionResult> AnalyzeHistory(
        [FromBody] HistoricalRiskAnalysisRequest request)
    {
        var result =
            await _riskEngineClient.AnalyzeHistoryAsync(request);

        return Ok(new
        {
            service = "RiskFlow API",
            analysis = result
        });
    }

    [HttpPost("analyze-market")]
    public async Task<IActionResult> AnalyzeMarket(
        [FromBody] MarketRiskAnalysisRequest request)
    {
        var result =
            await _riskEngineClient.AnalyzeMarketAsync(request);

        return Ok(new
        {
            service = "RiskFlow API",
            analysis = result
        });
    }
}