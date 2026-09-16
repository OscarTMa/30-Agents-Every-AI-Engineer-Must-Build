import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from legal_agent import LegalIntelligenceAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = LegalIntelligenceAgent()

    matter_query = (
        "Client operates an e-commerce marketplace and is sued in California federal court "
        "by a foreign competitor alleging improper online data extraction. Does the court have personal "
        "jurisdiction over the dispute, and what standard of care applies under Ninth Circuit precedent?"
    )
    jurisdiction = "Ninth Circuit"

    print("=== Legal Intelligence Agent Initialized ===")
    print(f"Conducting legal research and brief preparation for: '{jurisdiction}'...\n")

    result = agent.analyze_legal_matter(matter_query, jurisdiction)
    memo = result["memo"]
    verification = result["verification"]

    print("="*80)
    print("LEGAL RESEARCH MEMORANDUM")
    print("="*80)
    print(f"Matter Summary: {memo.matter_summary}\n")

    print("1. DECOMPOSED LEGAL ISSUES:")
    for issue in memo.decomposed_issues:
        print(f"   [{issue.issue_id}] {issue.description}")
        print(f"       Doctrine: {issue.relevant_doctrine}")

    print("\n2. DOCTRINAL SYNTHESIS & ANALYSIS:")
    print(memo.doctrinal_synthesis)

    print("\n3. CITATION VERIFICATION GATE REPORT:")
    print(f"   Total Citations Extracted:    {verification.total_citations}")
    print(f"   Verified Good-Law Authorities: {verification.verified_citations}")
    print(f"   Verification Status:          {'[PASS] Fully Verified' if verification.citations_verified else '[FAIL] Unverified Cites Found'}")
    print(f"   Citation Quality Score:       {verification.quality_score * 100:.0f}%")
    if verification.unverified_citations:
        print(f"   * Flagged Hallucinated Citations: {verification.unverified_citations}")

    print("\n4. STRATEGIC RECOMMENDATION:")
    print(memo.strategic_recommendation)

    # Demo de revisión de contrato
    print("\n" + "="*80)
    print("CONTRACT CLAUSE RISK AUDIT DEMO")
    print("="*80)
    clause_sample = "Supplier shall indemnify, defend, and hold harmless Customer without limitation against any and all liabilities."
    clause_audit = agent.contract_analyzer.evaluate_clause("Indemnification Clause", clause_sample)
    print(f"Clause:        {clause_audit.clause_title}")
    print(f"Risk Level:    [{clause_audit.risk_level}]")
    print(f"Risk Details:  {clause_audit.risk_explanation}")
    print(f"Proposed Fix:  {clause_audit.recommended_amendment}")