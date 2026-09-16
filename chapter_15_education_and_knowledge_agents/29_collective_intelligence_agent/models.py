from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Proposal:
    agent_id: str
    role: str
    content: str
    confidence: float

@dataclass
class EvaluationItem:
    evaluator_id: str
    proposal_agent_id: str
    score: float  # 0.0 to 10.0
    critique: str

@dataclass
class ConsensusSynthesis:
    rounds_executed: int
    consensus_score: float
    is_converged: bool
    final_rubric: str