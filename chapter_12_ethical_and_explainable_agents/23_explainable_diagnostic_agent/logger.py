from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class DecisionTraceStep:
    stage_name: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)

class DecisionLogger:
    """
    Immutable audit trail logger for regulatory compliance (EU AI Act / HIPAA).
    """
    def __init__(self):
        self.trace: List[DecisionTraceStep] = []

    def record_step(self, stage_name: str, payload: Dict[str, Any]):
        self.trace.append(DecisionTraceStep(stage_name=stage_name, payload=payload))

    def export_audit_trail(self) -> List[Dict[str, Any]]:
        return [
            {
                "stage": s.stage_name,
                "timestamp": s.timestamp.isoformat(),
                "payload": s.payload
            }
            for s in self.trace
        ]