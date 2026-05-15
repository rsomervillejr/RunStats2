import pytest
from src.app import create_app
from src.models import db

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

class TestRunsAPI:
    """Contract tests for /api/runs endpoints."""

    def test_post_runs_creates_run_with_splits(self, client):
        """Test POST /api/runs creates a new run entry with splits."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 6.2,
            "run_type": "race",
            "environment": "outdoor",
            "race_name": "City 10K",
            "race_distance_miles": 6.2,
            "notes": "Strong finish",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 1.0, "time_seconds": 355},
                {"split_index": 4, "distance_miles": 3.2, "time_seconds": 1140}
            ]
        }

        response = client.post('/api/runs', json=payload)
        assert response.status_code == 201

        data = response.get_json()
        assert 'id' in data
        assert data['date'] == '2026-05-07'
        assert data['total_distance_miles'] == 6.2
        assert data['run_type'] == 'race'
        assert data['environment'] == 'outdoor'
        assert data['race_name'] == 'City 10K'
        assert data['race_distance_miles'] == 6.2
        assert len(data['splits']) == 4

    def test_post_runs_validates_required_fields(self, client):
        """Test POST /api/runs validates required fields."""
        # Missing required fields
        payload = {
            "splits": [{"split_index": 1, "distance_miles": 1.0, "time_seconds": 360}]
        }

        response = client.post('/api/runs', json=payload)
        assert response.status_code == 400

    def test_post_runs_allows_race_without_metadata(self, client):
        """Test POST /api/runs allows race runs without optional race metadata."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 6.2,
            "run_type": "race",
            "environment": "outdoor",
            "race_name": None,
            "race_distance_miles": None,
            "notes": None,
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 1.0, "time_seconds": 355},
                {"split_index": 4, "distance_miles": 3.2, "time_seconds": 1140}
            ]
        }

        response = client.post('/api/runs', json=payload)
        assert response.status_code == 201

        data = response.get_json()
        assert data['run_type'] == 'race'
        assert data['race_name'] is None
        assert data['race_distance_miles'] is None
        assert data['notes'] is None

    def test_post_runs_normalizes_blank_race_name_and_zero_distance(self, client):
        """Test POST /api/runs normalizes blank race_name and zero race_distance_miles to null."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 6.2,
            "run_type": "race",
            "environment": "outdoor",
            "race_name": "",
            "race_distance_miles": 0,
            "notes": None,
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 1.0, "time_seconds": 355},
                {"split_index": 4, "distance_miles": 3.2, "time_seconds": 1140}
            ]
        }

        response = client.post('/api/runs', json=payload)
        assert response.status_code == 201

        data = response.get_json()
        assert data['race_name'] is None
        assert data['race_distance_miles'] is None
        assert data['notes'] is None

    def test_post_runs_validates_split_distances_sum(self, client):
        """Test POST /api/runs validates that split distances sum to total distance."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 6.2,
            "run_type": "workout",
            "environment": "outdoor",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 1.0, "time_seconds": 355},
                {"split_index": 4, "distance_miles": 2.0, "time_seconds": 720}  # Sum = 5.0, not 6.2
            ]
        }

        response = client.post('/api/runs', json=payload)
        assert response.status_code == 400

    def test_get_runs_returns_list(self, client):
        """Test GET /api/runs returns a list of runs."""
        response = client.get('/api/runs')
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, list)

    def test_get_runs_by_id_returns_run_detail(self, client):
        """Test GET /api/runs/{id} returns run detail with splits."""
        # First create a run
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 1.1, "time_seconds": 400}
            ]
        }

        create_response = client.post('/api/runs', json=payload)
        assert create_response.status_code == 201
        run_id = create_response.get_json()['id']

        # Now get the run detail
        response = client.get(f'/api/runs/{run_id}')
        assert response.status_code == 200

        data = response.get_json()
        assert data['id'] == run_id
        assert data['date'] == '2026-05-07'
        assert data['total_distance_miles'] == 3.1
        assert data['run_type'] == 'workout'
        assert data['environment'] == 'treadmill'
        assert len(data['splits']) == 3
        assert 'pace_seconds_per_mile' in data['splits'][0]

    def test_get_run_by_id_returns_null_optional_fields(self, client):
        """Test GET /api/runs/{id} returns null optional fields when not set."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 6.2,
            "run_type": "race",
            "environment": "outdoor",
            "race_name": None,
            "race_distance_miles": None,
            "notes": None,
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 1.0, "time_seconds": 355},
                {"split_index": 4, "distance_miles": 3.2, "time_seconds": 1140}
            ]
        }

        create_response = client.post('/api/runs', json=payload)
        assert create_response.status_code == 201
        run_id = create_response.get_json()['id']

        response = client.get(f'/api/runs/{run_id}')
        assert response.status_code == 200

        data = response.get_json()
        assert data['race_name'] is None
        assert data['race_distance_miles'] is None
        assert data['notes'] is None

    def test_get_runs_by_invalid_id_returns_404(self, client):
        """Test GET /api/runs/{invalid_id} returns 404."""
        response = client.get('/api/runs/999')
        assert response.status_code == 404

    def test_put_runs_updates_run(self, client):
        """Test PUT /api/runs/{id} updates an existing run."""
        # First create a run
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1200}]
        }

        create_response = client.post('/api/runs', json=payload)
        assert create_response.status_code == 201
        run_id = create_response.get_json()['id']

        # Update the run
        update_payload = {
            "date": "2026-05-08",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "outdoor",
            "notes": "Updated run",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1150}]
        }

        response = client.put(f'/api/runs/{run_id}', json=update_payload)
        assert response.status_code == 200

        data = response.get_json()
        assert data['date'] == '2026-05-08'
        assert data['environment'] == 'outdoor'
        assert data['notes'] == 'Updated run'
        assert data['splits'][0]['time_seconds'] == 1150