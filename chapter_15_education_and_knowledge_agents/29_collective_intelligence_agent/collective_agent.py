import os
import sys
from pathlib import Path
from typing import Optional

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from google import genai
from collaborative_agent import CollaborativeAgent
from consensus_engine import ConsensusEngine, ConsensusSynthesis

class CollectiveIntelligenceSystem:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

        self.pedagogy = CollaborativeAgent(
            agent_id="agent_pedagogy",
            role="Pedagogy Specialist",
            expertise=["scaffolding", "cognitive load", "formative feedback", "partial credit"],
            client=self.client
        )
        self.domain = CollaborativeAgent(
            agent_id="agent_domain",
            role="Domain Algorithm Expert",
            expertise=["algorithm correctness", "edge cases", "runtime complexity", "code style"],
            client=self.client
        )
        self.assessment = CollaborativeAgent(
            agent_id="agent_assessment",
            role="Assessment Specialist",
            expertise=["rubric validity", "inter-rater reliability", "objective grading criteria"],
            client=self.client
        )

        self.engine = ConsensusEngine(
            agents=[self.pedagogy, self.domain, self.assessment],
            client=self.client
        )

    def design_rubric(self, assignment_prompt: str) -> ConsensusSynthesis:
        return self.engine.run_consensus(assignment_prompt, max_rounds=2)