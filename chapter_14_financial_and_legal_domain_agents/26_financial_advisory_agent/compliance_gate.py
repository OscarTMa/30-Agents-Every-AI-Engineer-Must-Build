from dataclasses import dataclass
from typing import List

@dataclass
class ComplianceCheckResult:
    passed: bool
    violations: List[str]
    max_concentration_limit: float

class FinancialComplianceGate:
    """
    Enforces regulatory suitability and asset concentration boundaries.
    """
    def __init__(self, max_asset_concentration: float = 0.30):
        self.max_concentration = max_asset_concentration

    def validate_allocation(self, allocation_map: dict, client_risk_tolerance: str, composite_risk: float) -> ComplianceCheckResult:
        violations = []

        # 1. Suitability check against client tolerance
        if client_risk_tolerance.lower() == "conservative" and composite_risk > 4.5:
            violations.append(f"SUITABILITY: Composite risk ({composite_risk}) exceeds conservative limit (4.5).")
        elif client_risk_tolerance.lower() == "moderate" and composite_risk > 7.0:
            violations.append(f"SUITABILITY: Composite risk ({composite_risk}) exceeds moderate limit (7.0).")

        # 2. Concentration limits check
        for asset, weight in allocation_map.items():
            if weight > self.max_concentration:
                violations.append(
                    f"CONCENTRATION: Allocation in {asset} ({weight*100:.1f}%) exceeds max allowable limit ({self.max_concentration*100:.1f}%)."
                )

        return ComplianceCheckResult(
            passed=len(violations) == 0,
            violations=violations,
            max_concentration_limit=self.max_concentration
        )