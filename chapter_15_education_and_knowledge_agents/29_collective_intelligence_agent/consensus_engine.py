import time
from typing import List
from pydantic import BaseModel, Field
from google import genai
from models import Proposal, EvaluationItem, ConsensusSynthesis
from collaborative_agent import CollaborativeAgent
from client_provider import generate_structured

class SynthesizedRubricOutput(BaseModel):
    synthesized_rubric: str = Field(description="Unified hybrid rubric resolving trade-offs across all agents")
    consensus_rationale: str = Field(description="Explanation of how pedagogical, domain, and validity concerns were merged")

class ConsensusEngine:
    def __init__(self, agents: List[CollaborativeAgent], client: genai.Client):
        self.agents = agents
        self.client = client
        self.expertise_weights = {a.agent_id: 1.0 for a in agents}

    def run_consensus(self, problem: str, max_rounds: int = 1) -> ConsensusSynthesis:
        shared_history = ""
        last_scores = {}

        for r in range(max_rounds):
            print(f"  [Round {r+1}/{max_rounds}] Generating proposals and rotating adversarial critic...")
            critic_idx = r % len(self.agents)
            for i, a in enumerate(self.agents):
                a.is_critic = (i == critic_idx)

            proposals = [a.propose(problem, shared_history) for a in self.agents]

            evaluations = []
            for a in self.agents:
                for p in proposals:
                    if p.agent_id != a.agent_id:
                        evaluations.append(a.evaluate(p, problem))

            scores = {}
            for p in proposals:
                relevant = [e for e in evaluations if e.proposal_agent_id == p.agent_id]
                weighted_sum = sum(self.expertise_weights[e.evaluator_id] * e.score for e in relevant)
                total_w = sum(self.expertise_weights[e.evaluator_id] for e in relevant)
                scores[p.agent_id] = round(weighted_sum / total_w, 2) if total_w > 0 else 5.0

            last_scores = scores
            shared_history = "\n---\n".join([f"Proposal by {p.role}: {p.content[:150]}... (Score: {scores[p.agent_id]})" for p in proposals])

        avg_consensus = round(sum(last_scores.values()) / len(last_scores), 2)

        time.sleep(1)
        print("  [Synthesis Phase] Facilitator synthesizing final hybrid rubric...")
        prompt = f"""
You are the Collective Intelligence Synthesis Facilitator.
Synthesize the final grading rubric by unifying the best elements of each agent's proposal and resolving their critiques.

Problem: {problem}
Final Scored Proposals and Reviews:
{shared_history}

Produce a hybrid, professional rubric combining assessment clarity, formative feedback, and algorithmic rigor.
"""
        synth_data = generate_structured(self.client, prompt, SynthesizedRubricOutput)

        return ConsensusSynthesis(
            rounds_executed=max_rounds,
            consensus_score=avg_consensus,
            is_converged=True,
            final_rubric=synth_data.synthesized_rubric
        )