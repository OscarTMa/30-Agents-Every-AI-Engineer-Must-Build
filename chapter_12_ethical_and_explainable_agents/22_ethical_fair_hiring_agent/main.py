import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from fair_hiring_agent import FairHiringAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = FairHiringAgent()

    # Perfil con atributos demográficos sensibles que deben ser eliminados
    raw_candidate = {
        "name": "Jane Doe",
        "gender": "Female",
        "age": 34,
        "education_institution": "Wellesley College (Historically Women's Institution)",
        "skills": ["Python", "FastAPI", "Kubernetes", "PyTorch", "System Architecture"],
        "years_experience": 8,
        "past_achievements": "Led migration of microservices handling 2M req/sec with 99.99% uptime"
    }

    job_role = "Senior AI Infrastructure Engineer"

    print("=== Ethical Reasoning & Fair Hiring Agent ===")
    print("1. Layer 1: Anonymization & Deontic Pre-filtering...")
    anonymized = agent.anonymize_resume(raw_candidate)
    print("   Stripped sensitive fields: ['name', 'gender', 'age', 'education_institution']")
    print(f"   Anonymized Attributes: {list(anonymized.keys())}")

    print("\n2. Layer 2: Competency Scoring via LLM...")
    score_result = agent.evaluate_candidate("CANDIDATE-042", anonymized, job_role)
    print(f"   Candidate ID:  {score_result.candidate_id}")
    print(f"   Score:         {score_result.qualification_score}/100")
    print(f"   Skills Found:  {score_result.matched_skills}")
    print(f"   Verdict:       {score_result.selection_verdict}")

    print("\n3. Layer 3: Batch Fairness & Adverse Impact Audit (Simulated)...")
    # Tasa histórica: Grupo A (60%), Grupo B afectado históricamente (42%)
    bias_audit = agent.bias_detector.evaluate_batch_disparity(group_a_selection_rate=0.60, group_b_selection_rate=0.42)
    print(f"   Disparate Impact Ratio: {bias_audit.disparate_impact_ratio} (Safe harbor threshold: 0.80)")
    print(f"   Severity Classification: [{bias_audit.severity}]")
    print(f"   Enforced Mitigation:     {bias_audit.mitigation_strategy}")