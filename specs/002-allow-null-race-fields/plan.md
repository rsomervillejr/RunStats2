# Implementation Plan: Allow nullable race metadata and notes

**Branch**: `002-allow-null-race-fields` | **Date**: May 13, 2026 | **Spec**: `specs/002-allow-null-race-fields/spec.md`
**Input**: Feature specification from `/specs/002-allow-null-race-fields/spec.md`

## Summary

This feature updates the existing RunStats2 run entry flow to allow optional race metadata and notes fields to be omitted or explicitly null. The service layer and schema validation will continue enforcing required run fields, while permitting `race_name`, `race_distance_miles`, and `notes` to remain nullable.

## Technical Context

**Language/Version**: Python 3.8+ (Flask web service)  
**Primary Dependencies**: Flask, SQLAlchemy, Marshmallow, Flask-Migrate, python-dotenv, pytest  
**Storage**: PostgreSQL via SQLAlchemy ORM  
**Testing**: pytest (unit, integration, contract)  
**Target Platform**: Server-hosted web application with browser-based frontend  
**Project Type**: Web-service / full-stack backend with server-rendered UI and REST API  
**Performance Goals**: N/A for this feature  
**Constraints**: preserve existing run validation behavior; do not require optional race details for valid runs  
**Scale/Scope**: Single feature within existing RunStats2 application; no new service or external dependency required

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- The feature stays within the existing Flask + SQLAlchemy architecture.
- It does not add new persistence engines or external services.
- It preserves mandatory validation rules and does not expand attack surface beyond existing API behavior.
- No constitution violations are identified for this small behavior change.

## Project Structure

```text
src/
├── api/
├── models/
├── services/
├── templates/
├── static/
└── schemas.py

tests/
├── contract/
├── integration/
└── unit/

specs/002-allow-null-race-fields/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── run-api.md
```

**Structure Decision**: This is a web-service feature built on the existing single-project Flask repository layout. The change applies to the backend validation layer and the API contract while preserving the current `src/` and `tests/` structure.

## Complexity Tracking

No additional architectural complexity is required for this feature. The existing model and service layers are sufficient.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
