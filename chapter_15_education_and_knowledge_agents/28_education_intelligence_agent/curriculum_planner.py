import math
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Objective:
    obj_id: str
    title: str
    difficulty: float
    prerequisites: List[str]
    downstream_count: int

class CurriculumPlanner:
    """
    Ranks next objectives using Vygotsky's Zone of Proximal Development (ZPD) heuristic.
    """
    def __init__(self, mastery_threshold: float = 0.75):
        self.mastery_threshold = mastery_threshold
        self.objectives = [
            Objective("variables_types", "Variables & Types", 0.20, [], 3),
            Objective("conditionals", "Conditional Statements", 0.35, ["variables_types"], 2),
            Objective("loop_iteration", "For/While Loop Iteration", 0.45, ["variables_types", "conditionals"], 2),
            Objective("nested_control_flow", "Nested Loops & Breakpoints", 0.70, ["loop_iteration"], 1)
        ]

    def recommend_next(self, mastery_map: Dict[str, float]) -> List[Dict[str, Any]]:
        eligible = []
        for obj in self.objectives:
            current_m = mastery_map.get(obj.obj_id, 0.0)
            prereqs_met = all(mastery_map.get(p, 0.0) >= self.mastery_threshold for p in obj.prerequisites)

            if prereqs_met and current_m < self.mastery_threshold:
                # Cálculo de ZPD: delta óptimo = 0.20 por encima de la maestría actual
                delta = 0.20
                sigma = 0.25
                zpd_score = math.exp(-((obj.difficulty - current_m - delta) ** 2) / (2 * (sigma ** 2)))
                leverage_score = zpd_score * (1.0 + 0.15 * obj.downstream_count)
                eligible.append({
                    "objective": obj,
                    "current_mastery": current_m,
                    "score": round(leverage_score, 3)
                })

        eligible.sort(key=lambda x: x["score"], reverse=True)
        return eligible