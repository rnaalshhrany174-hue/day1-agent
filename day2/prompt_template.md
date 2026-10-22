# PROMPT TEMPLATE — CRUD API Builder (v1.1 - Filled)
 
ROLE: You are a senior Python backend engineer who writes production-quality, fully tested code.
 
TASK: Build a complete, runnable CRUD API for the entity below.
STACK: FastAPI + Pydantic v2
ENTITY: Asset (maintenance record)
FIELDS: asset_id, name, asset_type, location, criticality, status, last_inspection_date, operating_hours, notes
ENDPOINTS: 
  - GET /assets (list all with optional filters for status, criticality, asset_type, location)
  - GET /assets/{asset_id} (get single asset by id)
  - POST /assets (create new asset)
  - PUT /assets/{asset_id} (update existing asset)
  - DELETE /assets/{asset_id} (delete asset)
VALIDATION: asset_id must format correctly, criticality must be Low/Medium/High/Critical, status must be active/inactive/maintenance/inspection.
DATA: load maintenance_assets.csv at startup
TESTS: pytest covering happy path and failure cases for each endpoint.
 
OUTPUT FORMAT: one fenced code block per file, preceded by the file path. Files: main.py, models.py, test_api.py, README.md. No prose between files.
 
DEFINITION OF DONE: `uvicorn main:app` starts; `pytest -q` passes; no TODOs or placeholders.