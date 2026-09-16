from dataclasses import dataclass
from typing import List

@dataclass
class ContractClauseRisk:
    clause_title: str
    risk_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    risk_explanation: str
    recommended_amendment: str

class ContractRiskAnalyzer:
    """
    Evaluates commercial contract clauses against liability and indemnification baselines.
    """
    def evaluate_clause(self, title: str, text: str) -> ContractClauseRisk:
        t_lower = text.lower()
        if "unlimited liability" in t_lower or "indemnify and hold harmless without limitation" in t_lower:
            return ContractClauseRisk(
                clause_title=title,
                risk_level="CRITICAL",
                risk_explanation="Clause imposes uncapped indemnification and unlimited liability on the service provider.",
                recommended_amendment="Insert standard liability cap tied to aggregate fees paid in preceding 12 months."
            )
        elif "exclusive jurisdiction" in t_lower and "foreign" in t_lower:
            return ContractClauseRisk(
                clause_title=title,
                risk_level="HIGH",
                risk_explanation="Jurisdiction is assigned to an unfavorable foreign forum.",
                recommended_amendment="Negotiate neutral governing law and domestic arbitration."
            )
        else:
            return ContractClauseRisk(
                clause_title=title,
                risk_level="LOW",
                risk_explanation="Standard commercial terms conforming to routine boilerplate.",
                recommended_amendment="No amendment required."
            )