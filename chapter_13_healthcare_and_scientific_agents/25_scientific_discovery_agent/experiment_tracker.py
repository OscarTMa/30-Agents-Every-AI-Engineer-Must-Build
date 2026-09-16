from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class ExperimentResult:
    hypothesis_id: str
    predicted_properties: Dict[str, float]
    measured_properties: Dict[str, float]
    error_percentages: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.utcnow)

class ExperimentTracker:
    """
    Bridges digital in-silico predictions with physical laboratory measurements
    enabling closed-loop experiential learning (Level 4 Agent).
    """
    def __init__(self):
        self.history: List[ExperimentResult] = []

    def record_and_evaluate(self, hypothesis_id: str, predicted: Dict[str, float], measured: Dict[str, float]) -> ExperimentResult:
        errors = {}
        for prop, p_val in predicted.items():
            if prop in measured:
                m_val = measured[prop]
                err_pct = abs(p_val - m_val) / m_val * 100.0
                errors[prop] = round(err_pct, 2)

        record = ExperimentResult(
            hypothesis_id=hypothesis_id,
            predicted_properties=predicted,
            measured_properties=measured,
            error_percentages=errors
        )
        self.history.append(record)
        return record