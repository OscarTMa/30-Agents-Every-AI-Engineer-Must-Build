from typing import Dict, Any

COMPLIANCE_POLICIES: Dict[str, Dict[str, Any]] = {
    "PCI-DSS-3.3": {
        "title": "Do not log or expose raw Primary Account Numbers (PAN)",
        "severity": "CRITICAL",
        "description": "Full card numbers must never be printed in plain text or written to log files. Use mask_card_number()."
    },
    "HIPAA-164.312": {
        "title": "Protected Health Information (PHI) Redaction in Logs",
        "severity": "HIGH",
        "description": "Patient identifiers, SSN, diagnosis, and medical records must not be emitted to unencrypted application logs."
    }
}