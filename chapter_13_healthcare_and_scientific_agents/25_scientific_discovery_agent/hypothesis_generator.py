import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from gap_detector import KnowledgeGap

class PropertyPrediction(BaseModel):
    property_name: str = Field(description="Property identifier, e.g. glass_transition_temp_c, elongation_at_break_pct")
    predicted_value: float = Field(description="Quantified predicted numerical value")

class ProposedExperimentProtocol(BaseModel):
    synthesis_procedure: str = Field(description="Step-by-step laboratory synthesis methodology")
    characterization_techniques: List[str] = Field(description="Analytical methods, e.g. DSC, DMA, TGA")
    expected_target_properties: List[PropertyPrediction] = Field(description="List of quantified property predictions")

class ScientificHypothesis(BaseModel):
    hypothesis_id: str = Field(description="Unique identifier")
    formulation_name: str = Field(description="Chemical or structural formulation title")
    abductive_rationale: str = Field(description="Theoretical explanation bridging mechanism to the gap")
    novelty_assessment: str = Field(description="Why this extends beyond current literature")
    experimental_protocol: ProposedExperimentProtocol = Field(description="Concrete laboratory validation protocol")

class HypothesisSynthesisOutput(BaseModel):
    hypotheses: List[ScientificHypothesis] = Field(description="List of testable, actionable scientific hypotheses")

class ScientificHypothesisGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def formulate_hypotheses(self, gap: KnowledgeGap) -> List[ScientificHypothesis]:
        prompt = f"""
You are a senior scientific discovery agent specializing in materials science and polymer engineering.
Formulate a testable, novel scientific hypothesis grounded in abductive reasoning for the following knowledge gap.

Knowledge Gap:
- ID: {gap.gap_id}
- Domain: {gap.domain}
- Type: {gap.gap_type}
- Description: {gap.description}

Generate a concrete chemical formulation with quantified target properties (glass_transition_temp_c around 350-380, elongation_at_break_pct around 15-20) and laboratory protocol.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=HypothesisSynthesisOutput,
                temperature=0.0
            )
        )
        parsed = HypothesisSynthesisOutput.model_validate_json(response.text)
        return parsed.hypotheses