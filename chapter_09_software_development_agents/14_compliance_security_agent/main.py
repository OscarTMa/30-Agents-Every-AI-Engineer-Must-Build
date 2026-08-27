import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from compliance_agent import ComplianceSecurityAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    vulnerable_code = """import logging

logger = logging.getLogger("BillingService")

def process_patient_billing(patient_id, card_number, ssn, amount):
    logger.info(f"Initiating billing for SSN {ssn} and card {card_number}")
    return {"status": "success", "billed": amount}
"""

    agent = ComplianceSecurityAgent()
    print("Starting Compliance and Security Policy Audit...")
    report = agent.audit_and_remediate(vulnerable_code)

    decision_label = "[PASS] Compliant" if report.is_compliant else "[FAIL] Non-Compliant"
    print(f"\nAudit Decision: {decision_label}")
    print(f"Summary: {report.audit_summary}\n" + "=" * 80)

    for v in report.violations:
        print(f"Policy:      {v.rule_id}")
        print(f"Line Est:    {v.line_number_estimate}")
        print(f"Flagged:     {v.flagged_code_snippet}")
        print(f"Explanation: {v.explanation}")
        print(f"Remediation:\n{v.remediation_patch}")
        print("-" * 80)