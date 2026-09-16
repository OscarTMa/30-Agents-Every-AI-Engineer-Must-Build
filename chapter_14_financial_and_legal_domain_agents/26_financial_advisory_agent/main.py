import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from financial_agent import FinancialAdvisoryAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = FinancialAdvisoryAgent()

    client_profile = {
        "client_id": "RETAIL-CL-8841",
        "investable_assets_usd": 75000.0,
        "investment_horizon_years": 10,
        "risk_tolerance": "moderate",
        "primary_goal": "Long-term capital appreciation for retirement",
        "target_symbol": "BALANCED_INDEX"
    }

    print("=== Financial Advisory Agent Initialized ===")
    print(f"Generating personalized, compliant investment plan for Client ID: {client_profile['client_id']}...\n")

    result = agent.generate_plan(client_profile)
    metrics = result["risk_metrics"]
    report = result["report"]
    compliance = result["compliance"]

    print("="*80)
    print(f"STRATEGY: {report.portfolio_strategy_name.upper()}")
    print(f"Expected Annualized Return: {report.expected_annual_return_pct:.2f}%")
    print(f"Composite Risk Score: {metrics.composite_risk_score}/10 [{metrics.risk_category}] (Vol: {metrics.annualized_volatility:.2%}, Max DD: {metrics.max_drawdown:.2%})")
    print("="*80)

    print("\n1. RECOMMENDED ASSET ALLOCATION:")
    for alloc in report.allocations:
        print(f"   - {alloc.asset_class:<32}: {alloc.percentage_weight*100:5.1f}%")

    print("\n2. COMPLIANCE GATE STATUS:")
    if compliance.passed:
        print("   [APPROVED] Recommendation satisfies all regulatory suitability and concentration limits.")
    else:
        print("   [REJECTED] Violations detected:")
        for v in compliance.violations:
            print(f"     * {v}")

    print("\n3. FIDUCIARY RATIONALE & DISCLOSURES:")
    print(f"   Rationale:  {report.suitability_rationale}")
    print(f"   Disclosure: {report.risk_disclosure}")