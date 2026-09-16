from typing import List, Dict

class DualMemoryHierarchy:
    """
    Implements the dual-memory hierarchy:
    - Working Memory (RAM): Immediate turn buffer.
    - Semantic Memory (Disk): Long-term archival of key emotional/factual anchors.
    """
    def __init__(self, max_working_turns: int = 4):
        self.max_working_turns = max_working_turns
        self.working_memory: List[Dict[str, str]] = []
        self.semantic_memory: List[str] = []

    def save_turn(self, user_input: str, agent_output: str):
        self.working_memory.append({"role": "user", "content": user_input})
        self.working_memory.append({"role": "assistant", "content": agent_output})
        
        # Keep working memory within low-latency token window
        if len(self.working_memory) > self.max_working_turns * 2:
            self.working_memory = self.working_memory[-(self.max_working_turns * 2):]

    def archive_anchor(self, factual_anchor: str):
        """Explicitly stores important biographical/emotional context into long-term memory."""
        self.semantic_memory.append(factual_anchor)

    def get_working_context(self) -> str:
        if not self.working_memory:
            return "No previous conversation history."
        formatted = []
        for turn in self.working_memory:
            role = "User" if turn["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {turn['content']}")
        return "\n".join(formatted)

    def get_semantic_context(self) -> str:
        if not self.semantic_memory:
            return "No long-term archived records."
        return "\n".join([f"- {anchor}" for anchor in self.semantic_memory])