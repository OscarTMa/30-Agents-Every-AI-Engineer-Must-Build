from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from models import ZoneConfig, ZoneState, SensorReading, ActuatorCommand, ZoneType
from patterns import build_default_patterns
from controller import ProportionalControlManager

class SmartBuildingAgent:
    """
    Physical World Sensing Agent orchestrating sensor fusion,
    event pattern recognition, and closed-loop actuation.
    """
    def __init__(self):
        self.zones: Dict[str, ZoneConfig] = {}
        self.sensor_buffers: Dict[str, deque] = defaultdict(lambda: deque(maxlen=200))
        self.patterns = build_default_patterns()
        self.controller = ProportionalControlManager()

    def register_zone(self, config: ZoneConfig):
        self.zones[config.zone_id] = config

    def ingest_reading(self, zone_id: str, reading: SensorReading):
        self.sensor_buffers[zone_id].append(reading)

    def fuse_sensor_readings(self, zone_id: str) -> ZoneState:
        """Applies temporal filtering and fuses asynchronous noisy readings."""
        readings = self.sensor_buffers[zone_id]
        now = datetime.now()
        cutoff = now - timedelta(minutes=5)
        valid = [r for r in readings if r.timestamp >= cutoff]

        state = ZoneState(zone_id=zone_id, timestamp=now)
        
        temps = [r.value for r in valid if r.sensor_type == "temperature"]
        if temps:
            state.temperature_f = sum(temps) / len(temps)

        co2s = [r.value for r in valid if r.sensor_type == "co2"]
        if co2s:
            state.co2_ppm = sum(co2s) / len(co2s)

        motions = [r.value for r in valid if r.sensor_type == "motion"]
        state.occupancy_detected = any(m > 0.5 for m in motions) if motions else False

        return state

    def run_cognitive_cycle(self, zone_id: str) -> Tuple[ZoneState, List[str], List[ActuatorCommand]]:
        config = self.zones[zone_id]
        
        # 1. Sense & Model: Temporal Sensor Fusion
        state = self.fuse_sensor_readings(zone_id)

        # 2. Reason: Event Detection
        alerts = []
        for pattern in self.patterns:
            alert_msg = pattern.evaluate(state, config)
            if alert_msg:
                alerts.append(alert_msg)
        state.anomalies = alerts

        # 3. Act: Proportional Actuator Commands
        commands = self.controller.compute_commands(state, config)

        return state, alerts, commands