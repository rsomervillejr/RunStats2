# Quickstart

This feature updates the RunStats2 API and validation layer to allow nullable optional fields on run entries.

## Setup

1. Activate the Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Set `DATABASE_URL` and `SECRET_KEY`

4. Run database migrations:
   ```bash
   flask db upgrade
   ```

## Development Workflow

1. Update the feature schema and service logic.
2. Run targeted tests:
   ```bash
   pytest tests/unit/test_services.py tests/integration/test_run_creation.py tests/integration/test_run_editing.py
   ```
3. Confirm contract behavior with API client tests.

## Verification

- Create a run with omitted `race_name`, `race_distance_miles`, and `notes`.
- Update a run and leave optional fields null.
- Confirm API responses preserve null values for the optional fields.
