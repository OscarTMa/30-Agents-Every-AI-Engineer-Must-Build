import os
import sys
from pathlib import Path
from typing import Optional

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
from google import genai

from student_model import StudentModel
from curriculum_planner import CurriculumPlanner
from spaced_repetition import SpacedRepetitionScheduler
from client_provider import generate_socratic_feedback

load_dotenv(find_dotenv())

class SocraticFeedbackOutput(BaseModel):
    praise_acknowledgment: str = Field(description="Identifies what the learner did correctly")
    error_localization: str = Field(description="Guides the student to the problematic area without spoiling the fix")
    guiding_question: str = Field(description="Socratic question prompting independent conceptual discovery")
    scaffolding_hint_level: int = Field(description="Level of hint escalation from 1 to 4")

class EducationIntelligenceAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.student = StudentModel(student_id="ALEX-904")
        self.planner = CurriculumPlanner()
        self.scheduler = SpacedRepetitionScheduler()

    def generate_feedback(self, skill_id: str, exercise_desc: str, submission_code: str, error_context: str) -> SocraticFeedbackOutput:
        mastery = self.student.get_mastery_snapshot().get(skill_id, 0.15)
        recent_errs = self.student.skills.get(skill_id, None)
        recent_err_list = recent_errs.recent_errors if recent_errs else []

        prompt = f"""
You are an expert Socratic AI Programming Tutor.
The student made an error on an exercise. Provide scaffolding feedback that guides discovery without revealing the solution.

Target Skill: {skill_id} (Current Mastery Probability: {mastery*100:.1f}%)
Exercise: {exercise_desc}

Student Code Submission:
---
{submission_code.strip()}
---

Execution Error or Test Failure:
---
{error_context.strip()}
---

Recent Error History:
{recent_err_list}

Instructions:
1. Acknowledge what the student did right.
2. Localize the logical bug without giving the solution code.
3. Formulate a targeted, reflective guiding question.
4. Set hint level to 2 (Localization & Nudge).
"""
        return generate_socratic_feedback(self.client, prompt, SocraticFeedbackOutput)