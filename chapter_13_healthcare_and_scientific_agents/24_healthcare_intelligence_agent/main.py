import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from fhir_models import FHIRPatientRecord, FHIRVitalsObservation
from healthcare_agent import HealthcareIntelligenceAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = HealthcareIntelligenceAgent()

    # Paciente con sospecha clínica de sepsis / neumonía complicada
    patient = FHIRPatientRecord(
        patient_id="PAT-9842-EMERGENCY",
        age=68,
        gender="Male",
        vitals=FHIRVitalsObservation(
            heart_rate_bpm=112.0,
            systolic_bp=92.0,
            diastolic_bp=58.0,
            temperature_c=39.1,
            spo2_pct=91.0
        ),
        reported_symptoms=["Rigors and high fever for 24h", "Productive green sputum", "Acute lethargy and dizziness"],
        active_medications=["Metformin", "Lisinopril"]
    )

    print("=== Healthcare Intelligence Agent Initialized ===")
    print(f"Ingesting FHIR record for patient: {patient.patient_id}...")
    result = agent.process_patient(patient)

    print("\n" + "="*80)
    print(f"PRIMARY CLINICAL DIAGNOSIS: {result['report'].primary_diagnosis.upper()}")
    print(f"Bayesian Posterior Distribution: {result['posteriors']}")
    print("="*80)

    print(f"\n[SAFETY MONITOR STATUS] Escalation Required: {result['safety_eval'].requires_immediate_escalation}")
    print(f"Escalation Flag:   {result['safety_eval'].critical_condition_flagged}")
    print(f"Clinical Rationale: {result['safety_eval'].escalation_reason}")

    print("\n--- CLINICIAN-FACING ACTIONABLE DIRECTIVE ---")
    print(result['report'].clinician_actionable_plan)

    print("\n--- PATIENT-FACING PLAIN LANGUAGE SUMMARY ---")
    print(result['report'].patient_plain_language_summary)

    print(f"\n[AUDIT & PROVENANCE] Backed by {result['guideline'].provenance.source} v{result['guideline'].provenance.version}")