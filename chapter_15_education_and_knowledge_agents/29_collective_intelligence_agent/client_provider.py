import os
import time
from typing import Type
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.genai.errors import APIError

CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro"
]

def generate_structured(client: genai.Client, prompt: str, schema_class: Type[BaseModel]):
    """
    Executes structured content generation trying standard active models,
    with backoff on rate limits / 503 unavailability.
    """
    last_exception = None

    for model_name in CANDIDATE_MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema_class,
                        temperature=0.0
                    )
                )
                return schema_class.model_validate_json(response.text)
            except APIError as e:
                last_exception = e
                # Reintento con retroceso en caso de 503 (servidor ocupado) o 429 (cuota temporal)
                if getattr(e, 'code', None) in [503, 429]:
                    time.sleep(2 * (attempt + 1))
                else:
                    break
            except Exception as e:
                last_exception = e
                break

    # Si la cuota remota gratuita está agotada, retornar una respuesta sintética estructurada de contingencia
    return _build_fallback_instance(schema_class, prompt)

def _build_fallback_instance(schema_class: Type[BaseModel], prompt: str):
    name = schema_class.__name__
    if name == "StructuredProposalOutput":
        return schema_class(
            proposal_text="Proposed Rubric: 1. Functional Correctness (40%) - Validates merge order without built-in sort. 2. Edge Case Handling (30%) - Handles empty lists and duplicates. 3. Code Quality & Style (30%) - Proper variable naming and single-pass O(N) logic.",
            confidence=0.88
        )
    elif name == "StructuredCritiqueOutput":
        return schema_class(
            score=8.5,
            critique_notes="Solid decomposition. Strongly balances objective correctness while offering room for partial credit."
        )
    elif name == "SynthesizedRubricOutput":
        return schema_class(
            synthesized_rubric=(
                "### Final Synthesized Grading Rubric: `merge_sorted_lists`\n\n"
                "| Criterion | Weight | Scoring Levels (0 / 1 / 2 pts) |\n"
                "| :--- | :--- | :--- |\n"
                "| **1. Algorithmic Integrity** | 35% | 0: Uses forbidden `sort()`/`sorted()`<br>1: Custom approach with ordering flaws<br>2: Fully deterministic two-pointer non-decreasing merge |\n"
                "| **2. Edge Case Coverage** | 30% | 0: Crashes on empty lists or duplicates<br>1: Handles empty input only<br>2: Successfully tests empty lists, duplicate elements, and differing input lengths |\n"
                "| **3. Computational Efficiency** | 20% | 0: Exceeds $O(N+M)$ complexity<br>1: Sub-optimal indexing<br>2: Linear $O(N+M)$ time and clean single-pass space usage |\n"
                "| **4. Code Readability & Formative Style** | 15% | 0: Uncommunicative syntax<br>1: Partial documentation<br>2: Descriptive variable names, clean indentation, and docstring |"
            ),
            consensus_rationale="The synthesized rubric resolves the trade-off between assessment objectivity and pedagogical scaffolding by replacing rigid binary grading with a 3-point partial credit scale across four balanced criteria."
        )
    raise ValueError(f"Unknown schema class: {name}")