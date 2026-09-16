import os
import json
import numpy as np
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from risk_scorer import QuantitativeRiskScorer, RiskMetrics
from compliance_gate import FinancialComplianceGate

class AssetAllocationItem(BaseModel):
    asset_class: str = Field(description="Name of asset class or ticker (e.g., US Equities, Fixed Income)")
    percentage_weight: float = Field(description="Decimal weight, e.g. 0.35 for 35%")

class FinancialAdvisoryReport(BaseModel):
    portfolio_strategy_name: str = Field(description="Title of recommended investment strategy")
    allocations: List[AssetAllocationItem] = Field(description="Recommended asset allocation weights")
    expected_annual_return_pct: float = Field(description="Estimated annualized return percentage")
    suitability_rationale: str = Field(description="Regulatory suitability explanation matching client horizon and goals")
    risk_disclosure: str = Field(description="Formal regulatory risk warning and disclosures")

class FinancialAdvisoryAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.risk_scorer = QuantitativeRiskScorer()
        self.compliance_gate = FinancialComplianceGate(max_asset_concentration=0.35)

    def generate_plan(self, client_profile: dict) -> dict:
        # Step 1: Simulate asset historical return distributions and score risk
        simulated_market_returns = np.random.normal(0.0004, 0.012, 252)
        risk_metrics = self.risk_scorer.evaluate_asset(client_profile.get("target_symbol", "PORTFOLIO_CORE"), simulated_market_returns)

        # Step 2: Generate preliminary allocation via LLM reasoning
        prompt = f"""
You are a fiduciary Financial Advisory Agent.
Design a diversified portfolio allocation strictly obeying the client profile and risk metrics.

Client Profile:
{json.dumps(client_profile, indent=2)}

Quantitative Risk Assessment:
- Annualized Volatility: {risk_metrics.annualized_volatility}
- Max Drawdown: {risk_metrics.max_drawdown}
- 95% VaR: {risk_metrics.var_95}
- Composite Risk: {risk_metrics.composite_risk_score} [{risk_metrics.risk_category}]

Constraints:
- Total allocation weights MUST sum exactly to 1.0.
- Maximum allocation per individual asset class should not exceed 35% (0.35).
- Tailor strategy strictly to risk tolerance: {client_profile.get('risk_tolerance')}.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FinancialAdvisoryReport,
                temperature=0.0
            )
        )
        report = FinancialAdvisoryReport.model_validate_json(response.text)

        # Step 3: Run through deterministic Compliance Gate
        allocation_dict = {item.asset_class: item.percentage_weight for item in report.allocations}
        compliance_check = self.compliance_gate.validate_allocation(
            allocation_dict,
            client_profile.get("risk_tolerance", "moderate"),
            risk_metrics.composite_risk_score
        )

        return {
            "risk_metrics": risk_metrics,
            "report": report,
            "compliance": compliance_check
        }