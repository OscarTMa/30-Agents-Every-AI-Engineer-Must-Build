import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from legal_kb import LegalKnowledgeBase
from citation_verifier import CitationVerificationGate, CitationVerificationReport
from contract_analyzer import ContractRiskAnalyzer, ContractClauseRisk

class ExtractedLegalIssue(BaseModel):
    issue_id: str = Field(description="Identifier for the legal issue")
    description: str = Field(description="Discrete statutory or doctrinal question")
    relevant_doctrine: str = Field(description="Governing legal doctrine or rule")

class LegalResearchMemo(BaseModel):
    matter_summary: str = Field(description="Concise summary of the legal matter")
    decomposed_issues: List[ExtractedLegalIssue] = Field(description="Discrete legal questions identified")
    cited_precedents: List[str] = Field(description="Specific citations referenced in the analysis")
    doctrinal_synthesis: str = Field(description="Thorough legal reasoning and argument")
    strategic_recommendation: str = Field(description="Actionable guidance for litigation or negotiation counsel")

class LegalIntelligenceAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.kb = LegalKnowledgeBase()
        self.verifier = CitationVerificationGate(self.kb)
        self.contract_analyzer = ContractRiskAnalyzer()

    def analyze_legal_matter(self, matter_description: str, jurisdiction: str) -> dict:
        precedents = self.kb.search_precedents(jurisdiction)
        precedents_context = [
            {"citation": p.citation, "name": p.case_name, "court": p.court, "summary": p.summary}
            for p in precedents
        ]

        prompt = f"""
You are a senior Legal Intelligence and Research Agent.
Analyze the following legal matter for jurisdiction '{jurisdiction}'.
Strict Rule: You must ONLY cite precedents from the verified authority list below. Do not invent citations.

Verified Available Precedents:
{json.dumps(precedents_context, indent=2)}

Legal Matter:
"{matter_description}"

Decompose into discrete legal issues, cite governing precedents, and synthesize a litigation research memorandum.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LegalResearchMemo,
                temperature=0.0
            )
        )
        memo = LegalResearchMemo.model_validate_json(response.text)

        # Citation Verification Gate
        verification_report = self.verifier.verify_draft_citations(memo.cited_precedents)

        return {
            "memo": memo,
            "verification": verification_report
        }