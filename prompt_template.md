# PROMPT TEMPLATE — CRUD API Builder (v1.0)

ROLE: You are a senior Python backend engineer who writes production-quality, fully tested code.

TASK: Build a complete, runnable CRUD API for the entity below.
STACK: {{STACK}}                      # e.g. FastAPI + Pydantic v2
ENTITY: {{ENTITY}}                    # e.g. Asset (maintenance record)
FIELDS: {{FIELDS}}                    # paste the field list from the spec
ENDPOINTS: {{ENDPOINTS}}              # the 5 CRUD endpoints + filters
VALIDATION: {{VALIDATION_RULES}}      # id format, enum values, immutable id
DATA: load {{SEED_FILE}} at startup   # maintenance_assets.csv
TESTS: {{TEST_REQUIREMENTS}}          # pytest, happy + failure per endpoint

OUTPUT FORMAT: one fenced code block per file, preceded by the file path. Files: main.py, models.py, test_api.py, README.md. No prose between files.

DEFINITION OF DONE: `uvicorn main:app` starts; `pytest -q` passes; no TODOs or placeholders.