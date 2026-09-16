from dataclasses import dataclass, field
from typing import Dict, Any, List
from bkt_tracker import BKTTracker

@dataclass
class SkillState:
    p_mastery: float = 0.15
    attempts: int = 0
    recent_errors: List[str] = field(default_factory=list)
    reps: int = 0
    interval_days: int = 1
    ease_factor: float = 2.5

class StudentModel:
    def __init__(self, student_id: str):
        self.student_id = student_id
        self.bkt = BKTTracker()
        self.skills: Dict[str, SkillState] = {
            "variables_types": SkillState(p_mastery=0.85),
            "conditionals": SkillState(p_mastery=0.80),
            "loop_iteration": SkillState(p_mastery=0.25),
            "nested_control_flow": SkillState(p_mastery=0.10)
        }

    def record_attempt(self, skill_id: str, correct: bool, error_note: str = None):
        if skill_id not in self.skills:
            self.skills[skill_id] = SkillState()
        state = self.skills[skill_id]
        state.p_mastery = self.bkt.update(state.p_mastery, correct)
        state.attempts += 1
        if error_note and not correct:
            state.recent_errors.append(error_note)
            state.recent_errors = state.recent_errors[-5:]

    def get_mastery_snapshot(self) -> Dict[str, float]:
        return {s: state.p_mastery for s, state in self.skills.items()}