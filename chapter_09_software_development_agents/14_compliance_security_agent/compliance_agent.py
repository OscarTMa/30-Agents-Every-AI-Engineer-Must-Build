import os
import re
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from rules import COMPLIANCE_POLICIES

class ViolationItem(BaseModel):
    rule_id: str = Field(description="Policy identifier, e.g. 'PCI-DSS-3.3' or 'HIPAA-164.312'")
    line_number_estimate: int = Field(description="Approximate line number of violation")
    flagged_code_snippet: str = Field(description="Vulnerable code line or block")
    explanation: str = Field(description="Why this violates policy")
    remediation_patch: str = Field(description="Clean Python replacement code snippet")

class ComplianceAuditReport(BaseModel):
    is_compliant: bool = Field(description="True if no severe compliance violations are present")
    violations: List[ViolationItem] = Field(default_factory=list)
    audit_summary: str = Field(description="Executive compliance summary")

class ComplianceSecurityAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def audit_and_remediate(self, source_code: str) -> ComplianceAuditReport:
        prompt = f"""
You are an expert Security and Compliance Officer.
Audit the following Python source code against the active compliance policies.
If violations exist, flag them and provide a concrete remediation patch.

Active Policies:
{COMPLIANCE_POLICIES}

Target Code to Audit:
---
{source_code.strip()}
---
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ComplianceAuditReport,
                temperature=0.0
            )
        )
        return ComplianceAuditReport.model_validate_json(response.text)