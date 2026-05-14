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

class TestRunEditingIntegration:
    """Integration tests for run editing workflow."""

    def test_edit_run_change_basic_fields_integration(self, client):
        """Test editing a run to change basic fields."""
        # Create initial run
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "notes": "Original workout",
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
            "notes": "Updated workout - moved outside",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1150}]
        }

        response = client.put(f'/api/runs/{run_id}', json=update_payload)
        assert response.status_code == 200

        data = response.get_json()
        assert data['id'] == run_id
        assert data['date'] == '2026-05-08'
        assert data['environment'] == 'outdoor'
        assert data['notes'] == 'Updated workout - moved outside'
        assert data['splits'][0]['time_seconds'] == 1150

        # Verify in database
        run = RunEntry.query.get(run_id)
        assert run.date == date(2026, 5, 8)
        assert run.environment == 'outdoor'
        assert run.notes == 'Updated workout - moved outside'

        splits = MileSplit.query.filter_by(run_id=run_id).all()
        assert len(splits) == 1
        assert splits[0].time_seconds == 1150

    def test_edit_run_change_type_to_race_integration(self, client):
        """Test editing a workout run to become a race run."""
        # Create initial workout run
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "outdoor",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1200}]
        }

        create_response = client.post('/api/runs', json=payload)
        assert create_response.status_code == 201
        run_id = create_response.get_json()['id']

        # Update to race
        update_payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "race",
            "environment": "outdoor",
            "race_name": "Spring 5K",
            "race_distance_miles": 3.1,
            "notes": "Converted to race entry",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1100}]
        }

        response = client.put(f'/api/runs/{run_id}', json=update_payload)
        assert response.status_code == 200

        data = response.get_json()
        assert data['run_type'] == 'race'
        assert data['race_name'] == 'Spring 5K'
        assert data['race_distance_miles'] == 3.1
        assert data['notes'] == 'Converted to race entry'

        # Verify in database
        run = RunEntry.query.get(run_id)
        assert run.run_type == 'race'
        assert run.race_name == 'Spring 5K'
        assert float(run.race_distance_miles) == 3.1

    def test_edit_run_change_splits_integration(self, client):
        """Test editing a run to change split structure."""
        # Create initial run with one split
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 4.0,
            "run_type": "workout",
            "environment": "outdoor",
            "splits": [{"split_index": 1, "distance_miles": 4.0, "time_seconds": 1600}]
        }

        create_response = client.post('/api/runs', json=payload)
        assert create_response.status_code == 201
        run_id = create_response.get_json()['id']

        # Update to have multiple splits
        update_payload = {
            "date": "2026-05-07",
            "total_distance_miles": 4.0,
            "run_type": "workout",
            "environment": "outdoor",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 380},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 400},
                {"split_index": 3, "distance_miles": 1.0, "time_seconds": 390},
                {"split_index": 4, "distance_miles": 1.0, "time_seconds": 430}
            ]
        }

        response = client.put(f'/api/runs/{run_id}', json=update_payload)
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['splits']) == 4

        # Verify splits in database
        splits = MileSplit.query.filter_by(run_id=run_id).order_by(MileSplit.split_index).all()
        assert len(splits) == 4
        assert splits[0].split_index == 1
        assert splits[0].time_seconds == 380
        assert splits[3].split_index == 4
        assert splits[3].time_seconds == 430

    def test_edit_nonexistent_run_returns_404(self, client):
        """Test editing a non-existent run returns 404."""
        update_payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "outdoor",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1200}]
        }

        response = client.put('/api/runs/999', json=update_payload)
        assert response.status_code == 404

    def test_edit_run_validation_integration(self, client):
        """Test validation errors when editing runs."""
        # Create a valid run first
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "outdoor",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1200}]
        }

        create_response = client.post('/api/runs', json=payload)
        run_id = create_response.get_json()['id']

        # Try to update with invalid data
        invalid_payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "race",
            "environment": "outdoor",
            # Missing race_name and race_distance_miles
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1200}]
        }

        response = client.put(f'/api/runs/{run_id}', json=invalid_payload)
        assert response.status_code == 400