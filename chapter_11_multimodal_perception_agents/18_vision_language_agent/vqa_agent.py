import os
from PIL import Image
from typing import Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class VisualReasoningOutput(BaseModel):
    step_by_step_analysis: str = Field(description="Systematic CoT breakdown of spatial layout, objects, and visual cues")
    answer: str = Field(description="Direct, grounded conclusion derived strictly from visual evidence")

class VisionLanguageAgent:
    """
    Vision-Language Agent implementing Chain-of-Thought reasoning
    over visual assets and natural language queries.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def answer_visual_query(self, image_path: str, question: str) -> VisualReasoningOutput:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        image = Image.open(image_path)
        
        prompt = f"""
You are an expert Vision-Language analytical agent.
Analyze the provided image carefully and answer the user question using Chain-of-Thought reasoning.

User Question: "{question}"

Follow these steps:
1. Identify all primary visual features, entities, and spatial arrangements.
2. Examine specific contextual cues relevant to the question.
3. Derive a definitive answer grounded strictly in the visual evidence.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VisualReasoningOutput,
                temperature=0.0
            )
        )
        return VisualReasoningOutput.model_validate_json(response.text)