import os
from typing import Optional
from google import genai
from safety import SafetyLayer
from memory import DualMemoryHierarchy
from persona import PersonaEngine

class ConversationalAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.safety = SafetyLayer()
        self.memory = DualMemoryHierarchy()
        self.persona = PersonaEngine()

    def handle_turn(self, user_input: str) -> str:
        # Step 1: Deterministic Safety Check (Sentinel circuit breaker)
        if not self.safety.is_safe(user_input):
            return self.safety.get_crisis_protocol()

        # Step 2: Assemble Context from Memory Hierarchy
        working_ctx = self.memory.get_working_context()
        semantic_ctx = self.memory.get_semantic_context()

        # Step 3: Context-Augmented Prompt Construction
        prompt = f"""
{self.persona.get_system_instruction()}

=== LONG-TERM SEMANTIC ARCHIVE ===
{semantic_ctx}

=== RECENT WORKING MEMORY (DIALOG BUFFER) ===
{working_ctx}

=== CURRENT USER INPUT ===
User: {user_input}

Respond empathetically following all persona boundaries:
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        agent_reply = response.text.strip()

        # Step 4: Write back to memory
        self.memory.save_turn(user_input, agent_reply)
        return agent_reply