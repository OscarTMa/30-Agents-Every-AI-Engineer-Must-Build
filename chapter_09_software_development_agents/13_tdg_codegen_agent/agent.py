import os
import re
from typing import Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from test_runner import execute_pytest_in_sandbox

class TestSuiteSpec(BaseModel):
    test_code: str = Field(description="Complete pytest code including edge cases and assertion checks")

class ImplementationSpec(BaseModel):
    code: str = Field(description="Pure Python function implementation matching specifications")

def clean_python_code(raw_code: str) -> str:
    cleaned = re.sub(r"^```python\s*", "", raw_code, flags=re.MULTILINE)
    cleaned = re.sub(r"^```\s*$", "", cleaned, flags=re.MULTILINE)
    return cleaned.strip()

class TDGCodegenAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    def generate_test_suite(self, requirement: str) -> str:
        """Phase 1: RED (Tester Agent generates executable specification)."""
        prompt = f"""
You are a senior QA engineer. Write a comprehensive pytest test suite for the requirement.
Include standard cases, boundary conditions, and invalid inputs (raising ValueError).
Assume functions are imported directly from the root module namespace.

Requirement:
{requirement}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TestSuiteSpec,
                temperature=0.0
            )
        )
        return clean_python_code(TestSuiteSpec.model_validate_json(response.text).test_code)

    def synthesize_code(self, requirement: str, test_suite: str, error_context: str = "") -> str:
        """Phase 2 & Refine: GREEN (Developer Agent synthesizes and refines implementation)."""
        # Se construye la sección de error por separado para evitar barras invertidas dentro del f-string
        error_section = ""
        if error_context:
            error_section = f"PREVIOUS ATTEMPT FAILED WITH ERROR TRACE:\n{error_context}\nFix the implementation."

        prompt = f"""
You are a Python software engineer. Write the minimal clean implementation to make the tests pass.

Requirement:
{requirement}

Test Suite Contract:
{test_suite}

{error_section}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ImplementationSpec,
                temperature=0.0
            )
        )
        return clean_python_code(ImplementationSpec.model_validate_json(response.text).code)

    def run_tdg_loop(self, requirement: str, max_iterations: int = 3) -> dict:
        print(f"\n[TDG Agent: Red Phase] Generating Test Suite specification...")
        test_suite = self.generate_test_suite(requirement)
        print("Generated Tests Preview:")
        for line in test_suite.splitlines()[:10]:
            print(f"  | {line}")

        error_context = ""
        current_code = ""
        for iteration in range(1, max_iterations + 1):
            print(f"\n[TDG Agent: Green Phase] Iteration {iteration}/{max_iterations} - Generating Code...")
            current_code = self.synthesize_code(requirement, test_suite, error_context)
            
            print(f"[TDG Agent: Execution & Validation] Running pytest in sandbox...")
            passed, output = execute_pytest_in_sandbox(current_code, test_suite)

            if passed:
                print(f"[TDG Verdict] SUCCESS! All tests passed in iteration {iteration}.")
                return {
                    "passed": True,
                    "iterations": iteration,
                    "code": current_code,
                    "tests": test_suite,
                    "output": output
                }
            else:
                print(f"[TDG Verdict] FAILED. Feeding stack trace into next refinement loop.")
                error_context = output

        return {
            "passed": False,
            "iterations": max_iterations,
            "code": current_code,
            "tests": test_suite,
            "output": error_context
        }