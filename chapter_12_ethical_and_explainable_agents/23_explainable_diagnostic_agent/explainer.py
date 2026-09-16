import os
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class AudienceExplanations(BaseModel):
    clinician_explanation: str = Field(description="Technical diagnostic justification with feature weights & differential ranking")
    patient_explanation: str = Field(description="Clear, compassionate, jargon-free summary with practical next steps")

class ClinicalExplainer:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def generate_explanations(self, diagnosis: str, feature_attributions: Dict[str, float], confidence: float) -> AudienceExplanations:
        prompt = f"""
You are an expert Clinical Explainability Agent.
Generate two distinct audience-adapted explanations for this diagnostic finding:

1. Clinician Audience: Formal clinical reasoning, citing feature attribution weights (SHAP equivalents), differential considerations, and recommended verification tests.
2. Patient Audience: Compassionate, plain-language summary avoiding intimidating medical jargon, clearly explaining what was found and next steps with their doctor.

Diagnosis: {diagnosis}
Confidence: {confidence * 100:.1f}%
Feature Attributions (Relative Impact):
{feature_attributions}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AudienceExplanations,
                temperature=0.0
            )
        )
        return AudienceExplanations.model_validate_json(response.text)