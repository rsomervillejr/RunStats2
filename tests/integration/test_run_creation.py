import pytest
from src.app import create_app
from src.models import db, RunEntry, MileSplit
from datetime import date

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

class TestRunCreationIntegration:
    """Integration tests for run creation workflow."""

    def test_create_run_with_splits_integration(self, client):
        """Test complete run creation with splits through API."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "notes": "Test workout",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 1.1, "time_seconds": 400}
            ]
        }

        response = client.post('/api/runs', json=payload)
        assert response.status_code == 201

        data = response.get_json()
        assert 'id' in data
        assert data['date'] == '2026-05-07'
        assert data['total_distance_miles'] == 3.1
        assert data['run_type'] == 'workout'
        assert data['environment'] == 'treadmill'
        assert data['notes'] == 'Test workout'
        assert len(data['splits']) == 3

        # Verify data was saved to database
        run = RunEntry.query.get(data['id'])
        assert run is not None
        assert run.date == date(2026, 5, 7)
        assert float(run.total_distance_miles) == 3.1
        assert len(run.splits) == 3

        # Verify splits were saved
        splits = MileSplit.query.filter_by(run_id=run.id).order_by(MileSplit.split_index).all()
        assert len(splits) == 3
        assert splits[0].split_index == 1
        assert float(splits[0].distance_miles) == 1.0
        assert splits[0].time_seconds == 360

    def test_create_race_run_integration(self, client):
        """Test creating a race run with required metadata."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 6.2,
            "run_type": "race",
            "environment": "outdoor",
            "race_name": "City 10K",
            "race_distance_miles": 6.2,
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
        assert data['race_name'] == 'City 10K'
        assert data['race_distance_miles'] == 6.2

        # Verify in database
        run = RunEntry.query.get(data['id'])
        assert run.race_name == 'City 10K'
        assert float(run.race_distance_miles) == 6.2

    def test_create_run_validation_integration(self, client):
        """Test validation errors in run creation."""
        # Test missing required fields
        payload = {"splits": []}
        response = client.post('/api/runs', json=payload)
        assert response.status_code == 400

        # Test race without metadata
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 6.2,
            "run_type": "race",
            "environment": "outdoor",
            "splits": [{"split_index": 1, "distance_miles": 1.0, "time_seconds": 360}]
        }
        response = client.post('/api/runs', json=payload)
        assert response.status_code == 400

        # Test split distance mismatch
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 0.5, "time_seconds": 200}
            ]
        }
        response = client.post('/api/runs', json=payload)
        assert response.status_code == 400