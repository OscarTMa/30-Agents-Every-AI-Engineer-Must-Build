from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class PhysicalObjectState:
    object_id: str
    position_x: float
    position_y: float
    position_z: float
    weight_kg: float
    is_fragile: bool

@dataclass
class RobotBeliefState:
    robot_id: str = "ROBOT_ARM_01"
    current_x: float = 0.0
    current_y: float = 0.0
    current_z: float = 0.5
    current_payload_kg: float = 0.0
    nearest_human_distance_m: float = 3.5
    gripper_closed: bool = False
    objects: Dict[str, PhysicalObjectState] = field(default_factory=dict)

class WorldModel:
    """
    Maintains the continuous belief state b(s) over physical space and objects.
    All sensor readings update this internal representation.
    """
    def __init__(self):
        self.state = RobotBeliefState()
        # Inicializar objetos conocidos en el espacio de trabajo
        self.state.objects["package_A"] = PhysicalObjectState(
            object_id="package_A",
            position_x=1.2,
            position_y=0.4,
            position_z=0.1,
            weight_kg=4.2,
            is_fragile=True
        )
        self.state.objects["shelf_B"] = PhysicalObjectState(
            object_id="shelf_B",
            position_x=2.5,
            position_y=1.8,
            position_z=1.2,
            weight_kg=0.0,
            is_fragile=False
        )

    def get_state(self) -> RobotBeliefState:
        return self.state

    def update_position(self, x: float, y: float, z: float):
        self.state.current_x = x
        self.state.current_y = y
        self.state.current_z = z

    def update_payload(self, weight: float):
        self.state.current_payload_kg = weight

    def set_human_distance(self, distance_m: float):
        self.state.nearest_human_distance_m = distance_m