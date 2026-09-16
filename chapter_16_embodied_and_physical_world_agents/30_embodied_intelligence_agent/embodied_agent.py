import os
import sys
import time
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from world_model import WorldModel
from safety_monitor import SafetyMonitor, SafetyValidationResult
from control_interface import ControlInterface

class ProposedPhysicalAction(BaseModel):
    step_number: int = Field(description="Sequential order of operation")
    action_type: str = Field(description="Action verb: MOVE, GRASP, PLACE, HALT")
    target_x: float = Field(description="Target X in meters")
    target_y: float = Field(description="Target Y in meters")
    target_z: float = Field(description="Target Z in meters")
    rationale: str = Field(description="Physical explanation for why this step is taken")

class TaskPlan(BaseModel):
    plan_name: str = Field(description="Name of the physical manipulation sequence")
    actions: List[ProposedPhysicalAction] = Field(description="Chronological physical action steps")

class EmbodiedIntelligenceAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.world_model = WorldModel()
        self.safety_monitor = SafetyMonitor()
        self.controller = ControlInterface()

    def plan_task(self, operator_intent: str) -> TaskPlan:
        state = self.world_model.get_state()
        pkg = state.objects.get("package_A")
        shelf = state.objects.get("shelf_B")

        prompt = f"""
You are an Embodied Intelligence Planning Agent.
Decompose the operator's high-level goal into a sequence of admissible 3D kinematic actions.

Goal: "{operator_intent}"

Current World State Belief b(s):
- Robot at: ({state.current_x}, {state.current_y}, {state.current_z})
- Nearest Human Distance: {state.nearest_human_distance_m}m
- Package A pose: ({pkg.position_x}, {pkg.position_y}, {pkg.position_z}), weight: {pkg.weight_kg}kg, fragile: {pkg.is_fragile}
- Shelf B pose: ({shelf.position_x}, {shelf.position_y}, {shelf.position_z})

Rules:
1. Break down into discrete phases: MOVE to target, GRASP, MOVE to destination, PLACE.
2. Coordinates must fit within safe workspace bounds: X [-3, 3], Y [-3, 3], Z [0, 2.5].
"""
        for model_id in ["gemini-2.5-flash", "gemini-2.5-pro"]:
            try:
                response = self.client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=TaskPlan,
                        temperature=0.0
                    )
                )
                return TaskPlan.model_validate_json(response.text)
            except Exception:
                time.sleep(2)

        # Fallback determinista
        return TaskPlan(
            plan_name="Safe Pick and Place Package A to Shelf B",
            actions=[
                ProposedPhysicalAction(step_number=1, action_type="MOVE", target_x=1.2, target_y=0.4, target_z=0.2, rationale="Approach package A"),
                ProposedPhysicalAction(step_number=2, action_type="GRASP", target_x=1.2, target_y=0.4, target_z=0.1, rationale="Grasp package A securely"),
                ProposedPhysicalAction(step_number=3, action_type="MOVE", target_x=2.5, target_y=1.8, target_z=1.3, rationale="Transfer package A above shelf B"),
                ProposedPhysicalAction(step_number=4, action_type="PLACE", target_x=2.5, target_y=1.8, target_z=1.2, rationale="Place package A on shelf B")
            ]
        )

    def execute_plan(self, plan: TaskPlan) -> List[dict]:
        execution_trace = []
        for action in plan.actions:
            state = self.world_model.get_state()
            coords = (action.target_x, action.target_y, action.target_z)

            # Invariante de seguridad
            safety = self.safety_monitor.validate_action(action.action_type, coords, state)
            if not safety.is_safe:
                execution_trace.append({
                    "step": action.step_number,
                    "action": action.action_type,
                    "status": "[REJECTED BY SAFETY MONITOR]",
                    "reason": safety.reason
                })
                break

            # Despacho al controlador determinista
            res = self.controller.execute(action.action_type, coords)
            self.world_model.update_position(*coords)
            if action.action_type == "GRASP":
                self.world_model.update_payload(4.2)
            elif action.action_type == "PLACE":
                self.world_model.update_payload(0.0)

            execution_trace.append({
                "step": action.step_number,
                "action": action.action_type,
                "status": "[EXECUTED]",
                "target": coords,
                "latency_ms": res.duration_ms
            })
        return execution_trace