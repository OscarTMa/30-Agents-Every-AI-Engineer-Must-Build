import sys
from pathlib import Path

# Asegurar resolución de importaciones locales
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from education_agent import EducationIntelligenceAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = EducationIntelligenceAgent()

    print("=== Education Intelligence Agent Initialized ===")
    print(f"Student: {agent.student.student_id}")

    # 1. Recomendación curricular con ZPD (Zone of Proximal Development)
    print("\n1. CURRICULUM PLANNING (ZPD & Prerequisite Analysis):")
    recommendations = agent.planner.recommend_next(agent.student.get_mastery_snapshot())
    for r in recommendations:
        obj = r["objective"]
        print(f"   * [{obj.obj_id}] {obj.title} (Difficulty: {obj.difficulty:.2f} | Current Mastery: {r['current_mastery']:.2f} | ZPD Score: {r['score']})")

    # 2. Interacción y generación de feedback socrático
    target_skill = "loop_iteration"
    exercise = "Sum all even numbers from a list, but terminate early if a negative number is encountered."
    failing_code = """total = 0
for x in nums:
    if x < 0:
        break
    if x % 2 == 0:
        total += x
"""
    error_msg = "AssertionError: Expected sum of even numbers preceding negative element, but loop terminated before evaluating index 0 correctly."

    print(f"\n2. STUDENT INTERACTION & SOCRATIC FEEDBACK ON '{target_skill}':")
    feedback = agent.generate_feedback(target_skill, exercise, failing_code, error_msg)
    print(f"   [Praise]      {feedback.praise_acknowledgment}")
    print(f"   [Localize]    {feedback.error_localization}")
    print(f"   [Question]    {feedback.guiding_question}")
    print(f"   [Hint Level]  Level {feedback.scaffolding_hint_level}/4")

    # 3. Actualización de creencia latente vía Bayesian Knowledge Tracing (BKT)
    print("\n3. BAYESIAN KNOWLEDGE TRACING (BKT) BELIEF UPDATE:")
    prior_m = agent.student.skills[target_skill].p_mastery
    agent.student.record_attempt(target_skill, correct=False, error_note="Misplaced break condition in accumulation sequence")
    new_m = agent.student.skills[target_skill].p_mastery
    print(f"   Skill: {target_skill} | Prior P(L): {prior_m:.2f} --> Updated P(L): {new_m:.2f}")

    # 4. Programación de retención espaciada (SM-2)
    print("\n4. SPACED REPETITION (SM-2 RETENTION SCHEDULING):")
    sched = agent.scheduler.update_interval(reps=1, interval=6, ease=2.5, quality=3)
    print(f"   Retrieved successfully with guidance: Next review in {sched['interval_days']} days (Ease factor: {sched['ease_factor']})")