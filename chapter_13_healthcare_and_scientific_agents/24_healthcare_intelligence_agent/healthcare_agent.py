import os
import json
import numpy as np
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from fhir_models import FHIRPatientRecord
from knowledge_base import ClinicalKnowledgeBase
from safety_monitor import SafetyMonitor

class DiagnosisProbability(BaseModel):
    condition: str = Field(description="Name of condition, e.g. Sepsis, Pneumonia")
    probability: float = Field(description="Posterior probability score between 0.0 and 1.0")

class ClinicalDifferentialReport(BaseModel):
    primary_diagnosis: str = Field(description="Primary differential diagnosis candidate")
    differential_probabilities: List[DiagnosisProbability] = Field(description="Normalized posterior distribution over candidate conditions")
    clinician_actionable_plan: str = Field(description="Formal medical directive citing clinical guidelines and evidence")
    patient_plain_language_summary: str = Field(description="Clear, compassionate explanation avoiding medical jargon")

class HealthcareIntelligenceAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.kb = ClinicalKnowledgeBase()
        self.safety_monitor = SafetyMonitor(escalation_threshold=0.15)

    def bayesian_belief_update(self, prior: Dict[str, float], patient: FHIRPatientRecord) -> Dict[str, float]:
        """Performs Bayesian posterior belief update based on observed clinical vitals."""
        likelihoods = {}
        v = patient.vitals
        sepsis_weight = 1.0
        if v.temperature_c > 38.3 or v.temperature_c < 36.0:
            sepsis_weight *= 2.5
        if v.heart_rate_bpm > 90:
            sepsis_weight *= 2.0
        if v.systolic_bp < 100:
            sepsis_weight *= 2.0
        likelihoods["sepsis"] = sepsis_weight

        pneu_weight = 1.0
        if any("cough" in s.lower() for s in patient.reported_symptoms):
            pneu_weight *= 3.0
        if v.spo2_pct < 94:
            pneu_weight *= 2.0
        likelihoods["pneumonia"] = pneu_weight

        likelihoods["other_viral"] = 1.0

        unnormalized = {d: prior[d] * likelihoods[d] for d in prior}
        total = sum(unnormalized.values())
        return {d: round(val / total, 3) for d, val in unnormalized.items()}

    def process_patient(self, patient: FHIRPatientRecord) -> Dict[str, Any]:
        prior_beliefs = {"sepsis": 0.10, "pneumonia": 0.50, "other_viral": 0.40}
        posteriors = self.bayesian_belief_update(prior_beliefs, patient)

        safety_eval = self.safety_monitor.evaluate(posteriors)
        guideline_info = self.kb.retrieve_guideline("sepsis" if posteriors["sepsis"] > 0.4 else "pneumonia")

        prompt = f"""
You are a senior clinical intelligence agent.
Evaluate the patient case using the provided clinical observations, Bayesian posteriors, and clinical guidelines.

Patient Data:
- ID: {patient.patient_id} (Age: {patient.age}, {patient.gender})
- Vitals: Temp {patient.vitals.temperature_c}°C, HR {patient.vitals.heart_rate_bpm} bpm, BP {patient.vitals.systolic_bp}/{patient.vitals.diastolic_bp} mmHg, SpO2 {patient.vitals.spo2_pct}%
- Symptoms: {patient.reported_symptoms}

Calculated Bayesian Posterior Probabilities:
{json.dumps(posteriors, indent=2)}

Safety Monitor Status:
- Escalation Required: {safety_eval.requires_immediate_escalation}
- Reason: {safety_eval.escalation_reason}

Clinical Guideline Reference:
- Guideline Source: {guideline_info.provenance.source} (v{guideline_info.provenance.version})
- Recommended Protocol: {guideline_info.first_line_therapy}

Generate structured output with clinician actionable plans and patient plain language explanations.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ClinicalDifferentialReport,
                temperature=0.0
            )
        )
        report = ClinicalDifferentialReport.model_validate_json(response.text)

        return {
            "posteriors": posteriors,
            "safety_eval": safety_eval,
            "report": report,
            "guideline": guideline_info
        }