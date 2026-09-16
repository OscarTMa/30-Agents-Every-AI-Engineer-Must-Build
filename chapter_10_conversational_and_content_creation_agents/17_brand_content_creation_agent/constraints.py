from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class BrandGuidelines:
    """
    Brand consistency constraints modeled as a Constraint Satisfaction Problem (CSP).
    """
    tone: str = "authoritative-but-approachable"
    forbidden_terms: List[str] = field(
        default_factory=lambda: ["cheaper", "best-in-class", "industry-leading", "cheap", "magic bullet"]
    )

    def validate_content(self, content: str) -> Tuple[bool, List[str]]:
        violations = []
        content_lower = content.lower()
        for term in self.forbidden_terms:
            if term.lower() in content_lower:
                violations.append(term)
        return len(violations) == 0, violations