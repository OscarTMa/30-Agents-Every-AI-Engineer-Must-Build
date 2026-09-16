from dataclasses import dataclass
from typing import List, Dict

@dataclass
class BiasReport:
    disparate_impact_ratio: float
    is_biased: bool
    severity: str  # 'LOW', 'MEDIUM', 'HIGH'
    mitigation_strategy: str

class BiasDetector:
    """
    Computes statistical parity and Adverse Impact Ratio (Four-Fifths Rule: 0.80).
    """
    def evaluate_batch_disparity(self, group_a_selection_rate: float, group_b_selection_rate: float) -> BiasReport:
        if group_a_selection_rate == 0:
            ratio = 1.0
        else:
            ratio = group_b_selection_rate / group_a_selection_rate

        if ratio < 0.80:
            severity = "HIGH"
            strategy = "threshold_reweighting"
            is_biased = True
        elif ratio < 0.90:
            severity = "MEDIUM"
            strategy = "calibrated_score_adjustment"
            is_biased = True
        else:
            severity = "LOW"
            strategy = "none"
            is_biased = False

        return BiasReport(
            disparate_impact_ratio=round(ratio, 3),
            is_biased=is_biased,
            severity=severity,
            mitigation_strategy=strategy
        )