import os
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from deontic_rules import DeonticEthicsChecker
from bias_detector import BiasDetector, BiasReport

class CandidateScore(BaseModel):
    candidate_id: str = Field(description="Unique anonymized candidate identifier")
    qualification_score: float = Field(ge=0.0, le=100.0, description="Objective competency score")
    matched_skills: list[str] = Field(description="Concrete skills identified from resume")
    selection_verdict: str = Field(description="'RECOMMEND_INTERVIEW' or 'REJECT'")

class FairHiringAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.ethics_checker = DeonticEthicsChecker()
        self.bias_detector = BiasDetector()

    def anonymize_resume(self, raw_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Layer 1: Anonymization stripping protected quasi-identifiers."""
        cleaned = raw_resume.copy()
        for field in ["name", "gender", "age", "nationality", "photo", "education_institution"]:
            cleaned.pop(field, None)
        return cleaned

    def evaluate_candidate(self, candidate_id: str, anonymized_profile: Dict[str, Any], job_role: str) -> CandidateScore:
        """Layer 2: Objective Competency Evaluation."""
        # Deontic verification
        deontic_check = self.ethics_checker.validate_screening_action(anonymized_profile)
        if not deontic_check.is_permitted:
            raise ValueError(f"Deontic Policy Violation: {deontic_check.violation_rule}")

        prompt = f"""
You are an unbiased, objective technical recruitment agent.
Evaluate this candidate strictly on demonstrable technical competencies against the job role.

Job Role: {job_role}
Candidate Profile:
{json.dumps(anonymized_profile, indent=2)}

Score the candidate from 0 to 100 based solely on relevant skills and experience.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CandidateScore,
                temperature=0.0
            )
        )
        return CandidateScore.model_validate_json(response.text)