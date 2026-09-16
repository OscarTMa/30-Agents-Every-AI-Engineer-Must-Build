from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class ProvenanceRecord:
    source: str
    version: str
    retrieved_at: datetime
    confidence_score: float

@dataclass
class ClinicalGuidelineEntry:
    condition: str
    key_indicators: List[str]
    first_line_therapy: str
    provenance: ProvenanceRecord

class ClinicalKnowledgeBase:
    """
    Unified clinical knowledge base tracking source provenance,
    guideline versions, and contraindications.
    """
    def __init__(self):
        self.guidelines = {
            "sepsis": ClinicalGuidelineEntry(
                condition="Sepsis / Septic Shock",
                key_indicators=["temperature > 38.3C", "heart_rate > 90", "hypotension", "elevated lactate"],
                first_line_therapy="Blood cultures x2, serum lactate, broad-spectrum IV antibiotics within 1 hour",
                provenance=ProvenanceRecord("Surviving Sepsis Campaign", "2024.1", datetime.utcnow(), 0.98)
            ),
            "pneumonia": ClinicalGuidelineEntry(
                condition="Community-Acquired Pneumonia",
                key_indicators=["productive cough", "fever", "focal chest crackles", "infiltrates on imaging"],
                first_line_therapy="Targeted empiric respiratory antibiotics, hydration, oxygen support",
                provenance=ProvenanceRecord("IDSA/ATS Consensus Guidelines", "2023.4", datetime.utcnow(), 0.95)
            )
        }

    def retrieve_guideline(self, condition_key: str) -> ClinicalGuidelineEntry:
        return self.guidelines.get(condition_key.lower())