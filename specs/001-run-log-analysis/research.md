# Research: Run Log Analysis

## Decision: Flask + PostgreSQL

- Decision: Use Flask for the API layer and PostgreSQL as the primary database.
- Rationale: The user explicitly requested Flask with Postgres. Flask is lightweight and well-suited to a prototype REST API, while PostgreSQL provides strong relational integrity for runs and nested mile splits.
- Alternatives considered: Django/DRF (too heavy for this initial prototype), SQLite (contradicts requested Postgres choice), and no ORM (violates constitution requirement for SQLAlchemy).

## Decision: SQLAlchemy + Marshmallow

- Decision: Use SQLAlchemy for ORM mapping and Marshmallow for request/response validation.
- Rationale: The constitution mandates SQLAlchemy and strict validation. Marshmallow integrates cleanly with Flask and supports nested schemas for run entries and splits.
- Alternatives considered: Pydantic (good option, but Marshmallow is more common in Flask + SQLAlchemy patterns and is explicitly allowed by constitution guidance).

## Decision: Flask templates + Chart.js

- Decision: Use Flask's Jinja2 templating for HTML rendering and Chart.js for pace bar charts.
- Rationale: Keeps the prototype simple and self-contained within Flask, avoiding separate frontend build processes. Chart.js provides clean bar chart visualization for mile split paces without complex dependencies.
- Alternatives considered: React/Vue SPA (overkill for this prototype), pure HTML/JS (too basic for maintainable forms), server-side only rendering (limits interactivity for data entry).

## Decision: Nested run and split payloads

- Decision: Represent each run as a root object with an embedded list of mile splits.
- Rationale: This matches the domain model and avoids separate client-side synchronization for split data when creating or editing a run.
- Alternatives considered: separate split CRUD endpoints (rejected for initial scope complexity; nested payloads are easier for the first release).

## Key architecture conclusions

- The backend will enforce that every saved run has a date, total distance, classification, environment, and at least one split.
- Race entries will require race metadata when the run is tagged as a race.
- Fractional final split distances are supported by storing split distance explicitly and computing pace from split time.
- The API will provide pace values per split so charting can be rendered on the frontend without additional server-side work.
