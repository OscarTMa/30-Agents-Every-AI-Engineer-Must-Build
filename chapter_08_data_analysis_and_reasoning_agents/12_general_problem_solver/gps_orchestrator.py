import json
from typing import List, Dict, Any
from stages import GeneralProblemSolverStages

class GeneralProblemSolverOrchestrator:
    def __init__(self):
        self.stages = GeneralProblemSolverStages()
        self.strategy_log: List[Dict[str, Any]] = []

    def solve(self, research_question: str, max_iterations: int = 3) -> Dict[str, Any]:
        print(f"[GPS] Initiating autonomous meta-reasoning loop for research challenge:")
        print(f"      \"{research_question}\"")

        hint = ""
        for iteration in range(1, max_iterations + 1):
            print(f"\n" + "="*70 + f"\n[GPS] Execution Iteration {iteration}\n" + "="*70)

            # Stage 1: Decompose
            sub_problems = self.stages.stage1_decompose(research_question, hint=hint)
            print(f" -> Stage 1 (Decomposition):\n{json.dumps(sub_problems, indent=4)}")

            # Stage 2: Cross-domain Analogy Search
            analogies = self.stages.stage2_analogy_search(sub_problems)
            print(f" -> Stage 2 (Analogies):\n{json.dumps(analogies, indent=4)}")

            # Stage 3: Synthesize & Hypothesize
            hypothesis = self.stages.stage3_synthesize(sub_problems, analogies)
            print(f" -> Stage 3 (Synthesized Hypothesis):\n\"{hypothesis}\"")

            # Stage 4: Test & Reflect
            eval_result = self.stages.stage4_evaluate(hypothesis, iteration)
            print(f" -> Stage 4 (Rubric Evaluation):\n{json.dumps(eval_result, indent=4)}")

            # Stage 5: Meta-Learning & Refinement Gate
            log_entry = {
                "iteration": iteration,
                "confidence": eval_result["confidence"],
                "passed": eval_result["passed"],
                "hypothesis": hypothesis
            }

            if eval_result["passed"]:
                print(f"\n[GPS Verdict] PASSED with Confidence {eval_result['confidence']} (>= 0.70 threshold). Hypothesis accepted.")
                self.strategy_log.append(log_entry)
                return log_entry
            else:
                hint = "Previous decomposition was overly abstract. Re-focus strictly on quantitative graph-theoretic metrics (betweenness centrality, modularity, N-1 contingency) present in both food webs and electrical transmission grids."
                log_entry["refinement_hint"] = hint
                print(f"\n[GPS Verdict] BELOW THRESHOLD ({eval_result['confidence']} < 0.70). Activating Meta-Learning Engine with Refinement Hint.")
                self.strategy_log.append(log_entry)

        return self.strategy_log[-1]