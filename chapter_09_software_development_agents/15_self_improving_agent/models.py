from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class AdaptationType(str, Enum):
    PROMPT_UPDATE = "prompt_update"
    THRESHOLD_ADJUSTMENT = "threshold_adjustment"
    RETRIEVAL_STRATEGY = "retrieval_strategy"
    FEW_SHOT_INJECTION = "few_shot_injection"

class ImprovementHypothesis(BaseModel):
    source_signal: str = Field(description="Telemetry or failure pattern that triggered this hypothesis")
    adaptation_type: AdaptationType = Field(description="Categorical strategy for the adaptation")
    proposed_change: str = Field(description="Concrete adjustment to agent's prompt or heuristic")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score of proposed improvement")
    evidence_count: int = Field(description="Number of failure instances supporting this adaptation")
    rollback_safe: bool = Field(default=True, description="Whether change can be reverted instantaneously")

class BaselineMetrics(BaseModel):
    total_sessions_analyzed: int = Field(description="Total count of sessions in the analyzed batch")
    failure_rate: float = Field(description="Calculated baseline failure rate between 0.0 and 1.0")
    primary_failure_mode: str = Field(description="Most prevalent error signature identified")

class PlannerOutput(BaseModel):
    hypotheses: List[ImprovementHypothesis] = Field(description="List of concrete, evidence-backed adaptations")
    requires_human_review: bool = Field(description="True if proposed changes exceed automated risk boundaries")
    baseline_metrics: BaselineMetrics = Field(description="Structured baseline metrics from the telemetry batch")