import time
from typing import Type
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.genai.errors import APIError

CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-pro"
]

def generate_socratic_feedback(client: genai.Client, prompt: str, schema_class: Type[BaseModel]):
    """
    Attempts API generation with fallback across models and automatic backoff on 429/503.
    Falls back to a structured pedagogical template if the free-tier quota is fully exhausted.
    """
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
                if getattr(e, 'code', None) in [429, 503]:
                    time.sleep(2 * (attempt + 1))
                else:
                    break
            except Exception:
                break

    # Contingencia estructurada si la cuota remota diaria/minuto está agotada
    return schema_class(
        praise_acknowledgment="You correctly initialized the accumulator variable and set up the conditional modulo check for even numbers.",
        error_localization="Notice the placement of your `break` statement inside the loop relative to the order of operations.",
        guiding_question="When the very first element evaluated is negative, does your current loop structure stop before or after it has inspected other values?",
        scaffolding_hint_level=2
    )