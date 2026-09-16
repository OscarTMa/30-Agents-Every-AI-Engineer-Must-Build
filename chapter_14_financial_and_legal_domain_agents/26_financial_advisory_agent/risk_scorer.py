from dataclasses import dataclass
import numpy as np

@dataclass
class RiskMetrics:
    symbol: str
    annualized_volatility: float
    max_drawdown: float
    var_95: float
    composite_risk_score: float
    risk_category: str

class QuantitativeRiskScorer:
    """
    Computes multi-dimensional risk scores combining volatility,
    maximum drawdown, and Value-at-Risk (VaR 95%).
    """
    def evaluate_asset(self, symbol: str, simulated_returns: np.ndarray) -> RiskMetrics:
        # Annualized Volatility
        volatility = float(np.std(simulated_returns) * np.sqrt(252))

        # Cumulative returns and Maximum Drawdown
        cum_returns = np.cumprod(1 + simulated_returns)
        rolling_max = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - rolling_max) / rolling_max
        max_dd = float(np.min(drawdown))

        # Value-at-Risk at 95% confidence
        var_95 = float(np.percentile(simulated_returns, 5))

        # Scaled component scores (0 to 10 scale)
        vol_score = min(volatility / 0.05, 10.0)
        dd_score = min(abs(max_dd) / 0.05, 10.0)
        var_score = min(abs(var_95) / 0.03, 10.0)

        composite = round(0.40 * vol_score + 0.35 * dd_score + 0.25 * var_score, 2)

        if composite >= 7.0:
            category = "HIGH"
        elif composite >= 4.0:
            category = "MODERATE"
        else:
            category = "LOW"

        return RiskMetrics(
            symbol=symbol,
            annualized_volatility=round(volatility, 4),
            max_drawdown=round(max_dd, 4),
            var_95=round(var_95, 4),
            composite_risk_score=composite,
            risk_category=category
        )