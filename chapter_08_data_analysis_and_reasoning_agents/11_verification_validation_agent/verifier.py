import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from database import TRUSTED_DATABASE

class ExtractedClaim(BaseModel):
    claim_text: str = Field(description="Exact phrase asserting a verifiable fact")
    metric: str = Field(description="Metric under consideration, e.g., 'unemployment rate change', 'budget surplus'")
    value: str = Field(description="Raw numeric value asserted in the text, e.g., '5%', '$12 million'")
    entity: str = Field(description="Entity or region, e.g., 'Ottawa'")
    period: str = Field(description="Target timeframe, e.g., '2024'")

class ClaimListSchema(BaseModel):
    claims: List[ExtractedClaim]

class VerificationValidationAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def extract_claims(self, text: str) -> List[ExtractedClaim]:
        prompt = f"""
You are an expert investigative fact-checker. Extract all verifiable numeric statements from the following text.
Format output strictly into the schema.

Text to inspect:
"{text}"
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ClaimListSchema,
                temperature=0.0
            )
        )
        return ClaimListSchema.model_validate_json(response.text).claims

    def _map_to_db_key(self, metric: str, entity: str, period: str) -> str:
        m, e, p = metric.lower(), entity.lower(), str(period).lower()
        # Coincidencia flexible para variaciones temporales de Ottawa 2024 / last year
        if "unemployment" in m and "ottawa" in e and ("2024" in p or "last year" in p or "2023" in p or p == ""):
            return "ottawa_unemployment_rate_change_2024"
        if "budget surplus" in m and "ottawa" in e and ("2024" in p or "last year" in p or "fiscal" in p or p == ""):
            return "city_budget_surplus_2024"
        return ""

    def _parse_percentage(self, value_str: str) -> float:
        v = value_str.replace(" ", "").replace("%", "")
        return float(v) / 100.0

    def _parse_currency(self, value_str: str) -> float:
        v = value_str.replace("$", "").replace(",", "").strip().lower()
        multiplier = 1.0
        if "million" in v:
            multiplier = 1_000_000.0
            v = v.replace("million", "").strip()
        elif "billion" in v:
            multiplier = 1_000_000_000.0
            v = v.replace("billion", "").strip()
        return float(v) * multiplier

    def verify_claim(self, claim: ExtractedClaim) -> Dict[str, Any]:
        db_key = self._map_to_db_key(claim.metric, claim.entity, claim.period)
        if db_key not in TRUSTED_DATABASE:
            return {
                "claim": claim.claim_text,
                "status": "Unverified",
                "details": "No matching canonical record in trusted database.",
                "source": "N/A"
            }

        evidence = TRUSTED_DATABASE[db_key]
        actual_val = evidence["value"]
        
        try:
            if "%" in claim.value or "rate" in claim.metric.lower():
                claimed_num = self._parse_percentage(claim.value)
                # Compare absolute magnitude of change
                diff = abs(abs(claimed_num) - abs(actual_val))
                tolerance = 0.005  # 0.5 percentage points tolerance
                status = "Confirmed" if diff == 0 else ("Mostly True" if diff <= tolerance else "Contradicted")
                details = f"Claimed {claimed_num*100:.2f}%, actual {actual_val*100:.2f}% (Δ = {diff*100:.2f} pp)"
            else:
                claimed_num = self._parse_currency(claim.value)
                diff = abs(claimed_num - actual_val)
                tolerance = 500_000.0  # $500k rounding tolerance
                status = "Confirmed" if diff == 0 else ("Mostly True" if diff <= tolerance else "Contradicted")
                details = f"Claimed ${claimed_num:,.0f}, actual ${actual_val:,.0f} (Δ = ${diff:,.0f})"
        except Exception as e:
            return {"claim": claim.claim_text, "status": "Error", "details": f"Numeric parse failure: {e}"}

        return {
            "claim": claim.claim_text,
            "metric": claim.metric,
            "entity": claim.entity,
            "period": claim.period,
            "status": status,
            "details": details,
            "source": evidence["source"],
            "notes": evidence.get("notes", "")
        }