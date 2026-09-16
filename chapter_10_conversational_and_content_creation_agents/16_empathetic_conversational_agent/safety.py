class SafetyLayer:
    """
    Deterministic circuit breaker (Sentinel) positioned at the entry point.
    Intercepts crisis triggers and returns a strict protocol response.
    """
    def __init__(self):
        self.triggers = ["hurt myself", "suicide", "end my life", "harm", "kill myself"]

    def is_safe(self, text: str) -> bool:
        lower_text = text.lower()
        return not any(trigger in lower_text for trigger in self.triggers)

    def get_crisis_protocol(self) -> str:
        return (
            "I'm hearing that you're in a lot of pain. I am an AI companion and cannot "
            "provide emergency or crisis medical care. Please reach out immediately to a trusted "
            "professional or call/text the 988 Suicide & Crisis Lifeline (dial 988)."
        )