from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class DeonticValidationResult:
    is_permitted: bool
    violation_rule: str = ""
    action_type: str = "PERMIT"  # PERMIT, FORBID, MITIGATE

class DeonticEthicsChecker:
    """
    Evaluates actions against Deontic Logic axioms:
    O(phi): Obligatory, P(phi): Permitted, F(phi): Forbidden
    """
    FORBIDDEN_PROPERTIES = ["gender", "age", "ethnicity", "religion", "name", "nationality"]

    def validate_screening_action(self, candidate_features: Dict[str, Any]) -> DeonticValidationResult:
        # Check F(phi): Forbidden reliance on protected demographic features
        for sensitive in self.FORBIDDEN_PROPERTIES:
            if sensitive in candidate_features and candidate_features[sensitive] is not None:
                return DeonticValidationResult(
                    is_permitted=False,
                    violation_rule=f"F(demographic_reliance): Candidate {sensitive} must not be exposed to scoring engine.",
                    action_type="FORBID"
                )
        return DeonticValidationResult(is_permitted=True, action_type="PERMIT")