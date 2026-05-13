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

class TestRunViewingIntegration:
    """Integration tests for run viewing workflow."""

    def test_view_runs_list_integration(self, client):
        """Test viewing the list of runs ordered by date."""
        # Create multiple runs
        runs_data = [
            {
                "date": "2026-05-05",
                "total_distance_miles": 3.0,
                "run_type": "workout",
                "environment": "treadmill",
                "splits": [{"split_index": 1, "distance_miles": 3.0, "time_seconds": 1200}]
            },
            {
                "date": "2026-05-07",
                "total_distance_miles": 5.0,
                "run_type": "workout",
                "environment": "outdoor",
                "splits": [{"split_index": 1, "distance_miles": 5.0, "time_seconds": 1800}]
            },
            {
                "date": "2026-05-06",
                "total_distance_miles": 4.0,
                "run_type": "race",
                "environment": "outdoor",
                "race_name": "5K Fun Run",
                "race_distance_miles": 3.1,
                "splits": [{"split_index": 1, "distance_miles": 4.0, "time_seconds": 1500}]
            }
        ]

        # Create the runs
        for run_data in runs_data:
            response = client.post('/api/runs', json=run_data)
            assert response.status_code == 201

        # Get the runs list
        response = client.get('/api/runs')
        assert response.status_code == 200

        data = response.get_json()
        assert len(data) == 3

        # Verify ordering (newest first)
        assert data[0]['date'] == '2026-05-07'  # Newest
        assert data[1]['date'] == '2026-05-06'
        assert data[2]['date'] == '2026-05-05'  # Oldest

        # Verify summary data
        newest_run = data[0]
        assert newest_run['total_distance_miles'] == 5.0
        assert newest_run['run_type'] == 'workout'
        assert newest_run['environment'] == 'outdoor'
        assert newest_run['summary_pace_seconds_per_mile'] == 360.0  # 1800 / 5
        assert newest_run['split_count'] == 1

        # Verify race data
        race_run = data[1]
        assert race_run['run_type'] == 'race'
        assert race_run['race_name'] == '5K Fun Run'
        assert race_run['race_distance_miles'] == 3.1

    def test_view_run_detail_integration(self, client):
        """Test viewing detailed run information with splits and pace."""
        payload = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "notes": "Test workout with pace",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},  # 6:00/mi
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 390},  # 6:30/mi
                {"split_index": 3, "distance_miles": 1.1, "time_seconds": 440}   # ~6:40/mi
            ]
        }

        # Create the run
        create_response = client.post('/api/runs', json=payload)
        assert create_response.status_code == 201
        run_id = create_response.get_json()['id']

        # Get run detail
        response = client.get(f'/api/runs/{run_id}')
        assert response.status_code == 200

        data = response.get_json()
        assert data['id'] == run_id
        assert data['date'] == '2026-05-07'
        assert data['total_distance_miles'] == 3.1
        assert data['run_type'] == 'workout'
        assert data['environment'] == 'treadmill'
        assert data['notes'] == 'Test workout with pace'
        assert len(data['splits']) == 3

        # Verify splits are ordered and have pace
        splits = data['splits']
        assert splits[0]['split_index'] == 1
        assert splits[0]['distance_miles'] == 1.0
        assert splits[0]['time_seconds'] == 360
        assert splits[0]['pace_seconds_per_mile'] == 360.0

        assert splits[1]['split_index'] == 2
        assert splits[1]['distance_miles'] == 1.0
        assert splits[1]['time_seconds'] == 390
        assert splits[1]['pace_seconds_per_mile'] == 390.0

        assert splits[2]['split_index'] == 3
        assert splits[2]['distance_miles'] == 1.1
        assert splits[2]['time_seconds'] == 440
        assert abs(splits[2]['pace_seconds_per_mile'] - 400.0) < 0.1  # 440 / 1.1 ≈ 400

    def test_view_nonexistent_run_returns_404(self, client):
        """Test viewing a non-existent run returns 404."""
        response = client.get('/api/runs/999')
        assert response.status_code == 404

        data = response.get_json()
        assert 'error' in data