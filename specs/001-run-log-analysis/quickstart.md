# Quickstart: RunStats2 Backend Prototype

## Prerequisites

- Python 3.8 or newer
- PostgreSQL
- `git`
- Optional: Docker for containerized local development

## Setup

1. Clone the repository and switch to the feature directory if available:

```bash
cd /Users/ronsomerville/Documents/RunStats2
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install flask sqlalchemy flask-migrate marshmallow psycopg2-binary python-dotenv pytest
```

4. Configure local environment variables:

```bash
cat > .env <<'EOF'
FLASK_APP=src/app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:password@localhost:5432/runstats_dev
EOF
```

5. Create the PostgreSQL database:

```bash
createdb runstats_dev
```

6. Run database migrations:

```bash
flask db init
flask db migrate -m "Initial run log schema"
flask db upgrade
```

## Running the app

```bash
flask run
```

The API should be available at `http://127.0.0.1:5000`.

## Testing

Run unit and integration tests with pytest:

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## Notes

- This prototype includes both backend API and frontend web interface.
- The web interface provides view and edit modes for run logging.
- Chart.js is used for visualizing mile split paces in bar chart format.
- The backend will expose REST endpoints for history listing, run detail retrieval, creation, and editing.
