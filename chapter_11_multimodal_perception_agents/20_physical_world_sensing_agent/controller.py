from typing import List
from models import ZoneState, ZoneConfig, ActuatorCommand

class ProportionalControlManager:
    """
    Computes HVAC & Ventilation commands with deadband hysteresis to prevent short-cycling.
    """
    def compute_commands(self, state: ZoneState, config: ZoneConfig) -> List[ActuatorCommand]:
        commands = []
        if state.temperature_f is not None:
            target_midpoint = sum(config.target_temp_range) / 2.0
            error = state.temperature_f - target_midpoint

            # 1.5°F Deadband to prevent oscillation
            if abs(error) > 1.5:
                actuator = "hvac_cooling" if error > 0 else "hvac_heating"
                # Proportional gain: 20% intensity per degree error, capped at 100%
                intensity = min(100.0, abs(error) * 20.0)
                commands.append(ActuatorCommand(
                    zone_id=state.zone_id,
                    actuator_type=actuator,
                    intensity_pct=round(intensity, 1)
                ))

        # Ventilation control for CO2
        if state.co2_ppm is not None and state.co2_ppm > config.max_co2_ppm:
            excess = state.co2_ppm - config.max_co2_ppm
            vent_intensity = min(100.0, 40.0 + (excess / 10.0))
            commands.append(ActuatorCommand(
                zone_id=state.zone_id,
                actuator_type="ventilation_intake",
                intensity_pct=round(vent_intensity, 1)
            ))

        return commands