from dotenv import load_dotenv, find_dotenv
from gps_orchestrator import GeneralProblemSolverOrchestrator

load_dotenv(find_dotenv())

if __name__ == "__main__":
    gps = GeneralProblemSolverOrchestrator()
    question = "Can ecological network resilience principles inform strategies for preventing cascading failures in electrical power grids?"
    final_output = gps.solve(question)
    
    print("\n================ GPS PERSISTENT STRATEGY LOG ================")
    import json
    print(json.dumps(gps.strategy_log, indent=2))