import os
import json
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from models import PlannerOutput, ImprovementHypothesis

class SelfImprovingEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.adaptation_history: List[Dict[str, Any]] = []

    def analyze_feedback_and_plan(self, telemetry_logs: List[Dict[str, Any]]) -> PlannerOutput:
        """Critic & Planner loop: Synthesizes failure logs into improvement hypotheses."""
        prompt = f"""
You are a Meta-Learning Orchestrator for an AI agent platform.
Analyze the following operational telemetry logs and formulate structured improvement hypotheses.

Telemetry Logs:
{json.dumps(telemetry_logs, indent=2)}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PlannerOutput,
                temperature=0.0
            )
        )
        return PlannerOutput.model_validate_json(response.text)

    def apply_adaptation(self, hypothesis: ImprovementHypothesis, hitl_approved: bool = True):
        """Applies adaptation to agent's memory/configuration."""
        if not hitl_approved:
            print(f"[HITL Rejected] Adaptation rejected by human reviewer: {hypothesis.proposed_change}")
            return

        record = {
            "type": hypothesis.adaptation_type.value,
            "change": hypothesis.proposed_change,
            "confidence": hypothesis.confidence,
            "evidence_count": hypothesis.evidence_count,
            "status": "APPLIED_TO_PRODUCTION"
        }
        self.adaptation_history.append(record)
        print(f"[Engine Adapted] Applied: {hypothesis.proposed_change} (Confidence: {hypothesis.confidence})")