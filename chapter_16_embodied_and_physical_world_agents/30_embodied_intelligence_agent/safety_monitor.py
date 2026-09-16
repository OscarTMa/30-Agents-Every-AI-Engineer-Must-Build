from dataclasses import dataclass
from typing import Tuple
from world_model import RobotBeliefState

@dataclass
class SafetyValidationResult:
    is_safe: bool
    reason: str
    active_constraints: str

class SafetyMonitor:
    """
    Enforces the Admissible Action Set A_safe(s).
    Deterministic hard constraints evaluated before physical execution.
    """
    MAX_PAYLOAD_KG = 10.0
    MAX_VELOCITY_MPS = 1.5
    HUMAN_SAFETY_PERIMETER_M = 1.0
    WORKSPACE_X_BOUNDS = (-3.0, 3.0)
    WORKSPACE_Y_BOUNDS = (-3.0, 3.0)
    WORKSPACE_Z_BOUNDS = (0.0, 2.5)

    def validate_action(self, action_type: str, target_coords: Tuple[float, float, float], state: RobotBeliefState) -> SafetyValidationResult:
        tx, ty, tz = target_coords

        # 1. Human Proximity Invariant
        if state.nearest_human_distance_m < self.HUMAN_SAFETY_PERIMETER_M:
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Human worker within safety perimeter ({state.nearest_human_distance_m:.2f}m < {self.HUMAN_SAFETY_PERIMETER_M}m). E-STOP engaged.",
                active_constraints="HUMAN_CLEARANCE_REQUIRED"
            )

        # 2. Workspace Bounds Invariant
        if not (self.WORKSPACE_X_BOUNDS[0] <= tx <= self.WORKSPACE_X_BOUNDS[1] and
                self.WORKSPACE_Y_BOUNDS[0] <= ty <= self.WORKSPACE_Y_BOUNDS[1] and
                self.WORKSPACE_Z_BOUNDS[0] <= tz <= self.WORKSPACE_Z_BOUNDS[1]):
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Target position ({tx}, {ty}, {tz}) exceeds safe kinematic workspace envelope.",
                active_constraints=f"X:{self.WORKSPACE_X_BOUNDS}, Y:{self.WORKSPACE_Y_BOUNDS}, Z:{self.WORKSPACE_Z_BOUNDS}"
            )

        # 3. Payload Limit Invariant
        if action_type == "GRASP" and state.current_payload_kg > self.MAX_PAYLOAD_KG:
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Requested payload exceeds hardware torque limits ({state.current_payload_kg}kg > {self.MAX_PAYLOAD_KG}kg).",
                active_constraints=f"MAX_PAYLOAD_{self.MAX_PAYLOAD_KG}KG"
            )

        return SafetyValidationResult(is_safe=True, reason="Admissible within A_safe(s)", active_constraints="ALL_CONSTRAINTS_MET")