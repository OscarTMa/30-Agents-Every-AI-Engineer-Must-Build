import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from diagnostic_agent import DiagnosticAssistantAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = DiagnosticAssistantAgent()

    vitals_sample = {
        "heart_rate_bpm": 98,
        "spo2_pct": 92.5,
        "temperature_c": 38.6,
        "wbc_count_k_ul": 14.2
    }
    symptoms_sample = [
        "Productive cough with purulent sputum for 4 days",
        "Pleuritic chest pain on right side",
        "Shortness of breath upon mild exertion"
    ]

    print("=== Explainable Clinical Diagnostic Assistant ===")
    print("Processing patient vitals, symptoms, and generating dual-audience explanations...\n")

    report = agent.diagnose_and_explain(vitals_sample, symptoms_sample)

    print("="*80)
    print(f"PRIMARY ASSESSMENT: {report['diagnosis'].upper()}")
    print(f"Confidence: {report['confidence'].primary_probability * 100:.1f}% [{report['confidence'].confidence_tier}]")
    print(f"Epistemic Uncertainty: {report['confidence'].epistemic_uncertainty} | Aleatoric: {report['confidence'].aleatoric_uncertainty}")
    print("="*80)

    print("\n--- CLINICIAN-FACING EXPLANATION (SHAP Attribution & Clinical Rationale) ---")
    print(report['explanations'].clinician_explanation)

    print("\n--- PATIENT-FACING EXPLANATION (Jargon-Free & Actionable) ---")
    print(report['explanations'].patient_explanation)

    print("\n" + "="*80)
    print(f"AUDIT TRAIL LOGGED: {len(report['audit_trail'])} sequential decision stages recorded for regulatory compliance.")