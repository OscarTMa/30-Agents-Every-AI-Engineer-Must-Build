# 30 Agents Every AI Engineer Must Build
### Architectural Catalog & Implementation Roadmap (Chapters 5 to 16)
**Author:** [Oscar Tibaduiza](https://github.com/OscarTMa) | [Data Science Portfolio](https://www.datascienceportfol.io/oscartiba)

This repository serves as the central index and technical portfolio for the intelligent agent systems implemented from the book *30 Agents Every AI Engineer Must Build*. Each module is built as an independent, fully tested repository on Linux using Python 3.11 and the Google GenAI SDK.

---

## 1. Modular Repository Index

| Chapter | Domain / Core Focus | Key Agents | Repository Link |
| :--- | :--- | :--- | :--- |
| **Chapter 05** | **Memory Systems** | **#1** Working Memory, **#2** Episodic Memory, **#3** Semantic Memory | [chapter_05_memory_systems](https://github.com/OscarTMa/chapter_05_memory_systems) |
| **Chapter 06** | **Retrieval & Synthesis** | **#4** Deep Research, **#5** Multi-Source Synthesis | [chapter_06_retrieval_and_synthesis](https://github.com/OscarTMa/chapter_06_retrieval_and_synthesis) |
| **Chapter 07** | **Multi-Agent Systems** | **#6** Supervisor Router, **#7** Peer Debate | [chapter_07_multi_agent_systems](https://github.com/OscarTMa/chapter_07_multi_agent_systems) |
| **Chapter 08** | **Autonomous Coding** | **#8** Code Generation, **#9** Self-Healing Debugger | [chapter_08_autonomous_coding](https://github.com/OscarTMa/chapter_08_autonomous_coding) |
| **Chapter 09** | **Tool-Use & Resilience** | **#10** Dynamic Tool-Calling, **#11** API Fallback & Backoff | [chapter_09_tool_use_and_apis](https://github.com/OscarTMa/chapter_09_tool_use_and_apis) |
| **Chapter 10** | **Planning & Reasoning** | **#12** Tree-of-Thoughts (ToT), **#13** ReAct Reasoner | [chapter_10_planning_and_reasoning](https://github.com/OscarTMa/chapter_10_planning_and_reasoning) |
| **Chapter 11** | **Guardrails & Evaluation**| **#14** Output Guardrails, **#15** Self-Correction Evaluator | [chapter_11_guardrails_and_evaluation](https://github.com/OscarTMa/chapter_11_guardrails_and_evaluation) |
| **Chapter 12** | **Ethical & Explainable** | **#22** Fair Hiring Agent, **#23** Clinical Diagnostic Agent | [chapter_12_ethical_and_explainable_agents](https://github.com/OscarTMa/chapter_12_ethical_and_explainable_agents) |
| **Chapter 13** | **Healthcare & Science** | **#24** Healthcare Intelligence, **#25** Scientific Discovery | [chapter_13_healthcare_and_scientific_agents](https://github.com/OscarTMa/chapter_13_healthcare_and_scientific_agents) |
| **Chapter 14** | **Finance & Law** | **#26** Financial Advisory, **#27** Legal Intelligence | [chapter_14_financial_and_legal_domain_agents](https://github.com/OscarTMa/chapter_14_financial_and_legal_domain_agents) |
| **Chapter 15** | **Education & Consensus** | **#28** Education Intelligence, **#29** Collective Intelligence | [chapter_15_education_and_knowledge_agents](https://github.com/OscarTMa/chapter_15_education_and_knowledge_agents) |
| **Chapter 16** | **Physical World & Drone**| **#30** Embodied Intelligence, **#31** Domain Integration | [chapter_16_embodied_and_physical_world_agents](https://github.com/OscarTMa/chapter_16_embodied_and_physical_world_agents) |

---

## 2. Cross-Domain Engineering Foundations

* **Cognitive Memory Stack (Ch 5–7):** Dual-memory architecture balancing short-term working context, decayed episodic recall, and graph-structured semantic facts.
* **Execution & Reasoning Loops (Ch 8–11):** Self-healing code synthesis with AST parsing, OpenAPI tool-calling with exponential backoff, and Tree-of-Thoughts state-space search.
* **Regulated & High-Stakes Systems (Ch 12–14):** 
  * *Ethics:* Deontic quasi-identifier filtering and statistical adverse impact mitigation (4/5ths rule).
  * *Healthcare:* Bayesian POMDP belief updates over FHIR records with deterministic safety escalation ($\le 0.15$).
  * *Finance & Law:* Multi-dimensional portfolio risk scoring (VaR 95%) and strict citation verification to prevent hallucinated case law.
* **Pedagogy & Emergence (Ch 15):** Bayesian Knowledge Tracing (BKT) student models, Vygotsky Zone of Proximal Development (ZPD) curriculum planners, and rotating adversarial peer debate.
* **Physical Embodiment (Ch 16):** Asymmetric control loops ($0.1\text{--}1\text{ Hz}$ strategic planning vs $50\text{--}200\text{ Hz}$ deterministic PID/MPC control), hard safety invariant perimeters ($\mathcal{A}_{\text{safe}}(s)$ E-STOP), and conservative Unified Constraint Envelope fusion under subzero weather conditions.
