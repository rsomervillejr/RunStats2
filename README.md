# RunStats2

A Flask-based REST API for tracking running activities with PostgreSQL backend and Chart.js visualization.

## Features

- **Run Logging**: Record runs with date, distance, type (workout/race), environment, and notes
- **Mile Splits**: Track detailed pace data for each mile segment
- **Run History**: Browse and search past runs ordered by date
- **Pace Visualization**: Interactive charts showing pace trends across splits
- **Edit Runs**: Update existing run entries and splits
- **REST API**: Full CRUD operations for runs and splits

## Tech Stack

- **Backend**: Flask 2.3.3, SQLAlchemy 2.0.23, Marshmallow 3.20.1
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, Chart.js, Vanilla JavaScript
- **Testing**: pytest with contract, unit, and integration tests
- **Deployment**: Docker-ready

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip for dependency management

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RunStats2
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database URL and secret key
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
python -m flask run
```

Visit `http://localhost:5000` to access the web interface.

## API Documentation

### Runs Endpoints

- `GET /api/runs` - List all runs (newest first)
- `GET /api/runs/{id}` - Get detailed run information
- `POST /api/runs` - Create a new run
- `PUT /api/runs/{id}` - Update an existing run

### Request/Response Format

Runs include:
- Basic info: date, distance, type, environment, notes
- Race metadata: race_name, race_distance (when type is "race")
- Splits: array of mile segments with distance, time, and calculated pace

## Testing

Run the full test suite:
```bash
pytest
```

Run specific test types:
```bash
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/contract/      # API contract tests only
```

## Development

### Project Structure

```
src/
├── api/           # Flask API endpoints
├── models/        # SQLAlchemy database models
├── services/      # Business logic layer
├── static/        # CSS, JS, images
└── templates/     # Jinja2 HTML templates

tests/
├── contract/      # API contract tests
├── integration/   # End-to-end tests
└── unit/          # Unit tests

specs/             # Specification-driven development docs
```

### Adding New Features

This project uses Specification-Driven Development (SDD):

1. Create/update feature spec in `specs/`
2. Generate implementation plan with `/speckit.plan`
3. Create task breakdown with `/speckit.tasks`
4. Implement following TDD principles
5. Complete with `/speckit.implement`

## Deployment

### Docker

Build and run with Docker:
```bash
docker build -t runstats2 .
docker run -p 5000:5000 runstats2
```

### Production Considerations

- Set `SECRET_KEY` environment variable
- Configure PostgreSQL connection string
- Enable HTTPS in production
- Set up proper logging and monitoring
- Consider using a WSGI server like Gunicorn

## Contributing

1. Follow the SDD workflow for new features
2. Write tests first (TDD)
3. Ensure all tests pass
4. Update documentation as needed

## License

[Add your license here]