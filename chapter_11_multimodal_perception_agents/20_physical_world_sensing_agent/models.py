from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Tuple

class ZoneType(Enum):
    OFFICE = "office"
    SERVER_ROOM = "server_room"

@dataclass
class ZoneConfig:
    """Static invariant configuration."""
    zone_id: str
    zone_type: ZoneType
    target_temp_range: Tuple[float, float] = (68.0, 74.0)
    max_co2_ppm: float = 1000.0
    occupied_hours: Tuple[int, int] = (8, 18)

    def is_occupied_time(self, hour: int) -> bool:
        return self.occupied_hours[0] <= hour < self.occupied_hours[1]

@dataclass
class SensorReading:
    sensor_type: str  # 'temperature', 'co2', 'motion'
    value: float
    timestamp: datetime

@dataclass
class ZoneState:
    """Dynamic real-time digital twin state."""
    zone_id: str
    timestamp: datetime
    temperature_f: Optional[float] = None
    co2_ppm: Optional[float] = None
    occupancy_detected: bool = False
    anomalies: List[str] = field(default_factory=list)

@dataclass
class ActuatorCommand:
    zone_id: str
    actuator_type: str  # 'hvac_cooling', 'hvac_heating', 'ventilation'
    intensity_pct: float