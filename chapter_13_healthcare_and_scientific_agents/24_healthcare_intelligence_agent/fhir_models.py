from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class FHIRVitalsObservation:
    heart_rate_bpm: float
    systolic_bp: float
    diastolic_bp: float
    temperature_c: float
    spo2_pct: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class FHIRPatientRecord:
    patient_id: str
    age: int
    gender: str
    vitals: FHIRVitalsObservation
    reported_symptoms: List[str]
    active_medications: List[str]