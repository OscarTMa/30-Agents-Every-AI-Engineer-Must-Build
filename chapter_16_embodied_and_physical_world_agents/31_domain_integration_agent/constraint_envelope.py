from pydantic import BaseModel, Field
from typing import List, Dict

class DomainStatus(BaseModel):
    domain_name: str
    is_satisfied: bool
    details: str

class UnifiedConstraintEnvelope(BaseModel):
    corridor_id: str
    temperature_c: float
    wind_speed_kmh: float
    battery_soc: float
    active_notams_count: int
    parks_authorized: bool
    domains: List[DomainStatus]
    unified_envelope_green: bool = Field(description="True ONLY if ALL domains are satisfied (Conservative Fusion)")
    go_no_go_decision: str = Field(description="ARM_AND_EXECUTE or REJECT_MISSION")

def evaluate_envelope(corridor_id: str, temp_c: float, wind_kmh: float, soc: float, notams: int, parks_auth: bool) -> UnifiedConstraintEnvelope:
    domains = [
        DomainStatus(domain_name="Weather (Temp > -10C)", is_satisfied=(temp_c > -10.0), details=f"Ambient: {temp_c}°C"),
        DomainStatus(domain_name="Weather (Wind < 25 km/h)", is_satisfied=(wind_kmh < 25.0), details=f"Wind: {wind_kmh} km/h"),
        DomainStatus(domain_name="Battery (Departure SoC >= 30%)", is_satisfied=(soc >= 0.30), details=f"SoC: {soc*100:.0f}%"),
        DomainStatus(domain_name="Airspace (Transport Canada NOTAMs)", is_satisfied=(notams == 0), details=f"Active NOTAMs: {notams}"),
        DomainStatus(domain_name="Parks Canada Greenbelt Clearance", is_satisfied=parks_auth, details=f"Authorized: {parks_auth}")
    ]
    all_green = all(d.is_satisfied for d in domains)
    decision = "ARM_AND_EXECUTE" if all_green else "REJECT_MISSION"

    return UnifiedConstraintEnvelope(
        corridor_id=corridor_id,
        temperature_c=temp_c,
        wind_speed_kmh=wind_kmh,
        battery_soc=soc,
        active_notams_count=notams,
        parks_authorized=parks_auth,
        domains=domains,
        unified_envelope_green=all_green,
        go_no_go_decision=decision
    )