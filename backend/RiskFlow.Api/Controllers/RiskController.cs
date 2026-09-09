using Microsoft.AspNetCore.Mvc;
using RiskFlow.Api.Models;
using RiskFlow.Api.Services;
using RiskFlow.Api.Exceptions;

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
        try
        {
            var result =
                await _riskEngineClient.AnalyzeMarketAsync(request);

            return Ok(new
            {
                service = "RiskFlow API",
                analysis = result
            });
        }
        catch (RiskEngineException ex)
        {
            return StatusCode(
                ex.StatusCode,
                new
                {
                    error = "Market data unavailable",
                    message = ex.Message
                }
            );
        }
    }

    [HttpPost("analyze-portfolio")]
    public async Task<IActionResult> AnalyzePortfolio(
        [FromBody] PortfolioRiskRequest request)
    {
        try
        {
            var result =
                await _riskEngineClient.AnalyzePortfolioAsync(request);

            return Ok(new
            {
                service = "RiskFlow API",
                analysis = result
            });
        }
        catch (RiskEngineException ex)
        {
            return StatusCode(
                ex.StatusCode,
                new
                {
                    error = "Portfolio analysis failed",
                    message = ex.Message
                }
            );
        }
    }


    [HttpPost("simulate-portfolio")]
    public async Task<IActionResult> SimulatePortfolio(
        [FromBody] MonteCarloPortfolioRequest request)
    {
        try
        {
            var result =
                await _riskEngineClient.SimulatePortfolioAsync(request);

            return Ok(new
            {
                service = "RiskFlow API",
                simulation = result
            });
        }
        catch (RiskEngineException ex)
        {
            return StatusCode(
                ex.StatusCode,
                new
                {
                    error = "Portfolio simulation failed",
                    message = ex.Message
                }
            );
        }
    }
}