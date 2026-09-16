import time
from typing import Optional
from pydantic import BaseModel, Field
from google import genai
from models import Proposal, EvaluationItem
from client_provider import generate_structured

class StructuredProposalOutput(BaseModel):
    proposal_text: str = Field(description="Concrete rubric design proposal")
    confidence: float = Field(description="Confidence in this proposal from 0.0 to 1.0")

class StructuredCritiqueOutput(BaseModel):
    score: float = Field(description="Numerical quality score from 0 to 10")
    critique_notes: str = Field(description="Constructive critique identifying gaps, risks, or strengths")

class CollaborativeAgent:
    def __init__(self, agent_id: str, role: str, expertise: list[str], client: genai.Client):
        self.agent_id = agent_id
        self.role = role
        self.expertise = expertise
        self.client = client
        self.is_critic = False

    def propose(self, problem: str, shared_context: str) -> Proposal:
        time.sleep(1)
        prompt = f"""
You are a {self.role} specializing in {', '.join(self.expertise)}.
Problem: {problem}

Shared Context:
{shared_context if shared_context else "None (Initial round)."}

Draft your proposed rubric based on your domain expertise. Specify criteria and weights concisely.
"""
        data = generate_structured(self.client, prompt, StructuredProposalOutput)
        return Proposal(agent_id=self.agent_id, role=self.role, content=data.proposal_text, confidence=data.confidence)

    def evaluate(self, target_proposal: Proposal, problem: str) -> EvaluationItem:
        time.sleep(1)
        role_label = "Adversarial Critic" if self.is_critic else self.role
        prompt = f"""
You are acting as: {role_label} with domain expertise in {', '.join(self.expertise)}.
Problem: {problem}

Target Proposal to Review (Authored by {target_proposal.role}):
{target_proposal.content}

Score the proposal from 0 to 10 and give a concise critique.
"""
        data = generate_structured(self.client, prompt, StructuredCritiqueOutput)
        return EvaluationItem(
            evaluator_id=self.agent_id,
            proposal_agent_id=target_proposal.agent_id,
            score=data.score,
            critique=data.critique_notes
        )