namespace RiskFlow.Api.Exceptions;

public class RiskEngineException : Exception
{
    public int StatusCode { get; }

    public RiskEngineException(
        int statusCode,
        string message
    ) : base(message)
    {
        StatusCode = statusCode;
    }
}