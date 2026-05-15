import pytest
from unittest.mock import patch, MagicMock
from src.services.run_service import RunService
from src.models import RunEntry, MileSplit
from marshmallow import ValidationError
from datetime import date

class TestRunService:
    """Unit tests for RunService."""

    @patch('src.services.run_service.db')
    def test_create_run_success(self, mock_db):
        """Test successful run creation."""
        mock_session = MagicMock()
        mock_db.session = mock_session

        run_data = {
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

        # Mock the created run
        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.splits = []

        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run_class.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.create_run(run_data)

                assert result == mock_run
                mock_session.add.assert_called_once_with(mock_run)
                mock_session.commit.assert_called_once()

    def test_create_run_validation_error(self):
        """Test run creation with validation error."""
        invalid_data = {
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "splits": []
        }

        with pytest.raises(ValidationError):
            RunService.create_run(invalid_data)

    def test_create_run_split_distance_mismatch(self):
        """Test run creation with split distances not summing to total."""
        invalid_data = {
            "date": "2026-05-07",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "splits": [
                {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
                {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
                {"split_index": 3, "distance_miles": 0.5, "time_seconds": 200}  # Sum = 2.5, not 3.1
            ]
        }

        with pytest.raises(ValidationError):
            RunService.create_run(invalid_data)

    @patch('src.services.run_service.db')
    def test_create_run_allows_race_run_without_metadata(self, mock_db):
        """Test run creation accepts race runs with null optional race metadata."""
        mock_session = MagicMock()
        mock_db.session = mock_session

        run_data = {
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

        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.splits = []

        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run_class.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.create_run(run_data)

                assert result == mock_run
                mock_session.add.assert_called_once_with(mock_run)
                mock_session.commit.assert_called_once()

    @patch('src.services.run_service.db')
    def test_create_run_normalizes_blank_race_name_and_zero_distance(self, mock_db):
        """Test blank race_name and zero race_distance_miles normalize to null."""
        mock_session = MagicMock()
        mock_db.session = mock_session

        run_data = {
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

        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.splits = []

        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run_class.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.create_run(run_data)

                assert result == mock_run
                mock_session.add.assert_called_once_with(mock_run)
                mock_session.commit.assert_called_once()
                assert mock_run_class.call_args.kwargs['race_name'] is None
                assert mock_run_class.call_args.kwargs['race_distance_miles'] is None

    @patch('src.services.run_service.db')
    def test_update_run_normalizes_blank_race_name_and_zero_distance(self, mock_db):
        """Test update run normalizes blank race_name and zero race_distance_miles."""
        mock_session = MagicMock()
        mock_db.session = mock_session

        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.splits = [MagicMock()]

        update_data = {
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

        with patch('src.services.run_service.RunEntry') as mock_run_class:
            mock_run_class.query.get_or_404.return_value = mock_run
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_split_class.return_value = MagicMock()

                result = RunService.update_run(1, update_data)

                assert result == mock_run
                assert mock_run.race_name is None
                assert mock_run.race_distance_miles is None
                mock_session.commit.assert_called_once()

    @patch('src.services.run_service.db')
    def test_create_run_database_error(self, mock_db):
        """Test run update accepts race runs with null optional race metadata."""
        mock_session = MagicMock()
        mock_db.session = mock_session

        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.splits = [MagicMock()]

        update_data = {
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

        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run_class.query.get_or_404.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.update_run(1, update_data)

                assert result == mock_run
                mock_session.commit.assert_called_once()

    @patch('src.services.run_service.db')
    def test_create_run_database_error(self, mock_db):
        """Test run creation with database error."""
        mock_session = MagicMock()
        mock_session.commit.side_effect = Exception("Database error")
        mock_db.session = mock_session

        run_data = {
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

        with patch('src.services.run_service.RunEntry'):
            with pytest.raises(Exception):
                RunService.create_run(run_data)

            mock_session.rollback.assert_called_once()

    @patch('src.services.run_service.RunEntry')
    def test_get_runs_returns_list(self, mock_run_class):
        """Test get_runs returns formatted list."""
        # Mock runs
        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.date = date(2026, 5, 7)
        mock_run.total_distance_miles = 3.1
        mock_run.run_type = 'workout'
        mock_run.environment = 'treadmill'
        mock_run.race_name = None
        mock_run.race_distance_miles = None

        # Mock splits
        mock_split = MagicMock()
        mock_split.time_seconds = 360
        mock_split.distance_miles = 1.0
        mock_run.splits = [mock_split]

        mock_run_class.query.order_by.return_value.all.return_value = [mock_run]

        result = RunService.get_runs()

        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['summary_pace_seconds_per_mile'] == 360.0
        assert result[0]['split_count'] == 1

    @patch('src.services.run_service.RunEntry')
    def test_get_run_by_id_success(self, mock_run_class):
        """Test get_run_by_id returns formatted run detail."""
        # Mock run
        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.date = date(2026, 5, 7)
        mock_run.total_distance_miles = 3.1
        mock_run.run_type = 'workout'
        mock_run.environment = 'treadmill'
        mock_run.race_name = None
        mock_run.race_distance_miles = None
        mock_run.notes = 'Test run'
        mock_run.created_at = None
        mock_run.updated_at = None

        # Mock splits
        mock_split = MagicMock()
        mock_split.split_index = 1
        mock_split.distance_miles = 1.0
        mock_split.time_seconds = 360
        mock_run.splits = [mock_split]

        mock_run_class.query.get_or_404.return_value = mock_run

        result = RunService.get_run_by_id(1)

        assert result['id'] == 1
        assert result['date'] == '2026-05-07'
        assert len(result['splits']) == 1
        assert result['splits'][0]['pace_seconds_per_mile'] == 360.0

    @patch('src.services.run_service.db')
    def test_update_run_success(self, mock_db):
        """Test successful run update."""
        mock_session = MagicMock()
        mock_db.session = mock_session

        # Mock existing run
        mock_run = MagicMock()
        mock_run.id = 1
        mock_run.splits = [MagicMock()]  # Existing split

        update_data = {
            "date": "2026-05-08",
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "outdoor",
            "notes": "Updated run",
            "splits": [{"split_index": 1, "distance_miles": 3.1, "time_seconds": 1150}]
        }

        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run_class.query.get_or_404.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.update_run(1, update_data)

                assert result == mock_run
                mock_session.commit.assert_called_once()

    def test_update_run_validation_error(self):
        """Test run update with validation error."""
        invalid_data = {
            "total_distance_miles": 3.1,
            "run_type": "workout",
            "environment": "treadmill",
            "splits": []
        }

        with pytest.raises(ValidationError):
            RunService.update_run(1, invalid_data)