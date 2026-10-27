Day 3 Student Pack — Agentic Software Engineering
==================================================
Inputs needed from previous days: your .env (OpenRouter key) and venv.
New today: broken_tasks/ (5 tasks), flake8.

Setup:   pip install flake8     (everything else is already installed)
Lab 3.1: python repair_agent.py broken_tasks/task1
         then all tasks: python repair_agent.py broken_tasks/task*
Lab 3.2: edit MODELS in evaluate_models.py, then: python evaluate_models.py
         -> open evaluation_report.md
Lab 3.3: use review_checklist.md in the group review session
Lab 3.3 - Review Findings:
[HIGH] repair_agent.py — model outputs are verified by tests before application — owner: DELL
[MED] repair_agent.py — logs are properly recorded in results.jsonl — owner: DELL
[LOW] repair_agent.py — flake8 linting is integrated into the loop — owner: DELL