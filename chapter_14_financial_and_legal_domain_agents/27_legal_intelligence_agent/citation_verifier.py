from dataclasses import dataclass
from typing import List
from legal_kb import LegalKnowledgeBase, PrecedentAuthority

@dataclass
class CitationVerificationReport:
    total_citations: int
    verified_citations: int
    unverified_citations: List[str]
    citations_verified: bool
    quality_score: float

class CitationVerificationGate:
    """
    Cross-references every legal citation against authoritative ground truth
    to prevent AI citation hallucination.
    """
    def __init__(self, kb: LegalKnowledgeBase):
        self.kb = kb

    def verify_draft_citations(self, citations: List[str]) -> CitationVerificationReport:
        verified_count = 0
        unverified = []

        for cit in citations:
            match = self.kb.verify_citation(cit)
            if match and match.is_good_law:
                verified_count += 1
            else:
                unverified.append(cit)

        total = len(citations)
        passed = (total > 0 and verified_count == total)
        quality = verified_count / max(total, 1)

        return CitationVerificationReport(
            total_citations=total,
            verified_citations=verified_count,
            unverified_citations=unverified,
            citations_verified=passed,
            quality_score=round(quality, 2)
        )