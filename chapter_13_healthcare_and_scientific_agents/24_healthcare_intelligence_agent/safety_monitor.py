from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SafetyEvaluationResult:
    requires_immediate_escalation: bool
    critical_condition_flagged: str
    escalation_reason: str

class SafetyMonitor:
    """
    Deterministic safety circuit breaker enforcing cost-asymmetric
    escalation thresholds for critical conditions (Sepsis, MI, Stroke, PE).
    """
    CRITICAL_CONDITIONS = ["sepsis", "myocardial_infarction", "pulmonary_embolism", "stroke"]

    def __init__(self, escalation_threshold: float = 0.15):
        self.escalation_threshold = escalation_threshold

    def evaluate(self, differential_scores: Dict[str, float]) -> SafetyEvaluationResult:
        for condition in self.CRITICAL_CONDITIONS:
            score = differential_scores.get(condition, 0.0)
            if score >= self.escalation_threshold:
                return SafetyEvaluationResult(
                    requires_immediate_escalation=True,
                    critical_condition_flagged=condition.upper(),
                    escalation_reason=f"Estimated risk of {condition.upper()} is {score*100:.1f}%, exceeding safety threshold ({self.escalation_threshold*100:.1f}%)."
                )
        return SafetyEvaluationResult(
            requires_immediate_escalation=False,
            critical_condition_flagged="",
            escalation_reason="All critical risks are below conservative safety escalation boundaries."
        )