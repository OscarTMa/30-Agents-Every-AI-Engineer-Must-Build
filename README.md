# 30 Agents Every AI Engineer Must Build: Production Architecture & Implementation
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Google GenAI SDK](https://img.shields.io/badge/Google%20GenAI-v1.0+-green.svg)](https://ai.google.dev/)
[![CI/CD Pipelines](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange.svg)](https://github.com/OscarTMa)
[![Author](https://img.shields.io/badge/Author-Oscar%20Tibaduiza-purple.svg)](https://www.datascienceportfol.io/oscartiba)

<div align="center">
  <img src="assets/Title.jpg" alt="30 Agents Every AI Engineer Must Build Cover" width="340"/>
  <p><em>Reference Architecture implementations based on the book by Imran Ahmad, PhD (Packt Publishing).</em></p>
</div>

---

## Overview

This repository houses the end-to-end production implementation, mathematical modeling, and automated verification suites for the intelligent agent systems outlined in **"30 Agents Every AI Engineer Must Build"**. 

Moving beyond raw API prompting, each chapter is structured as a resilient, self-contained architecture featuring:
* **Strict Guardrails & Deterministic Invariants:** Hard safety boundary checks, deontic demographic filtering, and fiduciary concentration limits.
* **Hybrid Reasoning Systems:** Probabilistic Bayesian frameworks (BKT, POMDP) fused with modern LLM reasoning loops.
* **Production-Grade CI/CD:** GitHub Actions workflows automated with exponential backoffs, fallback models, and rate-limit pacing against high-throughput API demands.

---

## Architectural Breakdown & Repository Index

| Chapter Module | Core Agent Architectures | Key Mechanisms & Mathematical Foundations | Status |
| :--- | :--- | :--- | :---: |
| **`chapter_06_knowledge_agents`** | Knowledge Retrieval & Synthesis | Vector Indexing, Graph Traversal, Cross-Document Grounding | `Verified` |
| **`chapter_07_tool_orchestration_agents`** | Dynamic Tool-Use & APIs | Declarative Dispatch, OpenAPI Ingestion, Fault Recovery | `Verified` |
| **`chapter_08_data_analysis_and_reasoning_agents`** | Data Analysis, V&V, Problem Solver | OLS Statistical Modeling, Fact-Checking Tolerance Deltas, 5-Stage Meta-Reasoning | `Verified` |
| **`chapter_09_software_development_agents`** | TDG CodeGen, Security Sentinel, Self-Improving | Test-Driven Generation (TDG Red/Green), AST Static Vulnerability Checks, Reflexion | `Verified` |
| **`chapter_10_conversational_and_content_creation_agents`** | Empathetic Dialogue & Brand SMPA Pipeline | Dual-Memory System, Crisis Safety Intervention (988), Style Consistency Verification | `Verified` |
| **`chapter_11_multimodal_perception_agents`** | Vision-Language, Acoustic Sentiment, Sensing | Multimodal Visual CoT, Valence-Arousal-Dominance (VAD) Prosody, HVAC Deadband Control | `Verified` |
| **`chapter_12_ethical_and_explainable_agents`** | Fair Hiring & Explainable Diagnostics | EEOC 4/5ths Disparate Impact Mitigation, SHAP Attribution, Calibrated Uncertainty | `Verified` |
| **`chapter_13_healthcare_and_scientific_agents`** | Clinical Decision & Autonomous Discovery | FHIR Schema Normalization, Sepsis POMDP Alerting ($>15\%$), Closed-Loop Discovery | `Verified` |
| **`chapter_14_financial_and_legal_domain_agents`** | Quantitative Advisory & Legal Verification | VaR (95%), Max Drawdown, Fiduciary Concentration ($\le 35\%$), Good-Law Citation Filter | `Verified` |
| **`chapter_15_education_and_knowledge_agents`** | Pedagogical Guidance & Deliberation | Bayesian Knowledge Tracing (BKT), Vygotsky ZPD Scheduling, Rotating Adversarial Peer Debate | `Verified` |
| **`chapter_16_embodied_and_physical_world_agents`** | Embodied Control & Domain Integration | Asymmetric Control Loops ($0.1\text{--}1\text{ Hz}$ vs $50\text{--}200\text{ Hz}$), E-STOP hard perimeter ($1.0\text{ m}$), Subzero Flight Envelope Fusion | `Verified` |

---

## Technical Highlights

* **Resilience Against API Constraints:** Custom client wrappers with exponential backoff handling Google Gemini `429 RESOURCE_EXHAUSTED` and `503 UNAVAILABLE` conditions.
* **Deterministic Safety Overrides:** Physical interrupt loops in robotics and automated escalation protocols in healthcare workflows guarantee deterministic safety before actuation.
* **Automated CI/CD Verification:** Every agent is executed and tested in isolated runner environments on Ubuntu with automated dependency tracking.

---

## Getting Started

1. **Clone the repository:**
```bash
   git clone [https://github.com/OscarTMa/30-Agents-Every-AI-Engineer-Must-Build.git](https://github.com/OscarTMa/30-Agents-Every-AI-Engineer-Must-Build.git)
   cd 30-Agents-Every-AI-Engineer-Must-Build
```

2. **Set up virtual environment:**

```Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Configure credentials:**

```Bash
echo "GOOGLE_API_KEY=your_actual_key_here" > .env
```

4. **Run any chapter test pipeline:**

```Bash
python chapter_16_embodied_and_physical_world_agents/30_embodied_intelligence_agent/main.py
```

## Author & Contact
Engineer: Oscar Tibaduiza

GitHub: @OscarTMa

Portfolio: datascienceportfol.io/oscartiba
