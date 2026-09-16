from typing import List, Callable, Optional
from models import ZoneState, ZoneConfig

class EventPattern:
    def __init__(self, name: str, severity: str, condition: Callable[[ZoneState, ZoneConfig], bool], template: str):
        self.name = name
        self.severity = severity
        self.condition = condition
        self.template = template

    def evaluate(self, state: ZoneState, config: ZoneConfig) -> Optional[str]:
        if self.condition(state, config):
            return f"[{self.severity.upper()}] {self.template.format(zone_id=state.zone_id, temp=state.temperature_f, co2=state.co2_ppm)}"
        return None

def build_default_patterns() -> List[EventPattern]:
    return [
        EventPattern(
            name="critical_server_thermal_breach",
            severity="critical",
            condition=lambda s, c: c.zone_type == c.zone_type.SERVER_ROOM and s.temperature_f is not None and s.temperature_f > 78.0,
            template="Critical server room thermal spike in {zone_id}: {temp:.1f}°F!"
        ),
        EventPattern(
            name="high_co2_occupancy_breach",
            severity="warning",
            condition=lambda s, c: s.co2_ppm is not None and s.co2_ppm > c.max_co2_ppm,
            template="Air quality degraded in {zone_id}: CO2 at {co2:.0f} ppm exceeds threshold."
        ),
        EventPattern(
            name="unexpected_after_hours_motion",
            severity="alert",
            condition=lambda s, c: s.occupancy_detected and not c.is_occupied_time(s.timestamp.hour),
            template="Security notice: Unexpected after-hours occupancy detected in {zone_id}."
        )
    ]