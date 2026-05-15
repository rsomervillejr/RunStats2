import pytest
from unittest.mock import patch, MagicMock
from src.services.run_service import RunService
from marshmallow import ValidationError
from datetime import date


def test_create_run_success():
    """Test successful run creation."""
    run_data = {
        "date": "2026-05-07",
        "total_distance_miles": 3.1,
        "run_type": "workout",
        "environment": "treadmill",
        "splits": [
            {"split_index": 1, "distance_miles": 1.0, "duration_mmss": "06:00"},
            {"split_index": 2, "distance_miles": 1.0, "duration_mmss": "06:05"},
            {"split_index": 3, "distance_miles": 1.1, "duration_mmss": "06:40"}
        ]
    }

    mock_session = MagicMock()

    with patch('src.services.run_service.db') as mock_db:
        mock_db.session = mock_session
        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run = MagicMock()
                mock_run_class.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.create_run(run_data)

                assert result == mock_run
                mock_session.add.assert_called_once_with(mock_run)
                mock_session.commit.assert_called_once()


def test_create_run_validation_error():
    """Test run creation with validation error."""
    invalid_data = {
        "total_distance_miles": 3.1,
        "run_type": "workout",
        "environment": "treadmill",
        "splits": []
    }

    with pytest.raises(ValidationError):
        RunService.create_run(invalid_data)


def test_create_run_split_distance_mismatch():
    """Test run creation with split distances not summing to total."""
    invalid_data = {
        "date": "2026-05-07",
        "total_distance_miles": 3.1,
        "run_type": "workout",
        "environment": "treadmill",
        "splits": [
            {"split_index": 1, "distance_miles": 1.0, "duration_mmss": "06:00"},
            {"split_index": 2, "distance_miles": 1.0, "duration_mmss": "06:05"},
            {"split_index": 3, "distance_miles": 0.5, "duration_mmss": "03:20"}
        ]
    }

    with pytest.raises(ValidationError):
        RunService.create_run(invalid_data)


def test_create_run_allows_race_run_without_metadata():
    """Test run creation accepts race runs with null optional race metadata."""
    run_data = {
        "date": "2026-05-07",
        "total_distance_miles": 6.2,
        "run_type": "race",
        "environment": "outdoor",
        "race_name": None,
        "race_distance_miles": None,
        "notes": None,
        "splits": [
            {"split_index": 1, "distance_miles": 1.0, "duration_mmss": "06:00"},
            {"split_index": 2, "distance_miles": 1.0, "duration_mmss": "06:05"},
            {"split_index": 3, "distance_miles": 1.0, "duration_mmss": "05:55"},
            {"split_index": 4, "distance_miles": 3.2, "duration_mmss": "19:00"}
        ]
    }

    mock_session = MagicMock()

    with patch('src.services.run_service.db') as mock_db:
        mock_db.session = mock_session
        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run = MagicMock()
                mock_run_class.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.create_run(run_data)

                assert result == mock_run
                mock_session.add.assert_called_once_with(mock_run)
                mock_session.commit.assert_called_once()


def test_create_run_normalizes_blank_race_name_and_zero_distance():
    """Test blank race_name and zero race_distance_miles normalize to null."""
    run_data = {
        "date": "2026-05-07",
        "total_distance_miles": 6.2,
        "run_type": "race",
        "environment": "outdoor",
        "race_name": "",
        "race_distance_miles": 0,
        "notes": None,
        "splits": [
            {"split_index": 1, "distance_miles": 1.0, "duration_mmss": "06:00"},
            {"split_index": 2, "distance_miles": 1.0, "duration_mmss": "06:05"},
            {"split_index": 3, "distance_miles": 1.0, "duration_mmss": "05:55"},
            {"split_index": 4, "distance_miles": 3.2, "duration_mmss": "19:00"}
        ]
    }

    mock_session = MagicMock()

    with patch('src.services.run_service.db') as mock_db:
        mock_db.session = mock_session
        with patch('src.services.run_service.RunEntry') as mock_run_class:
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_run = MagicMock()
                mock_run_class.return_value = mock_run
                mock_split_class.return_value = MagicMock()

                result = RunService.create_run(run_data)

                assert result == mock_run
                mock_session.add.assert_called_once_with(mock_run)
                mock_session.commit.assert_called_once()
                assert mock_run_class.call_args.kwargs['race_name'] is None
                assert mock_run_class.call_args.kwargs['race_distance_miles'] is None


def test_update_run_normalizes_blank_race_name_and_zero_distance():
    """Test update run normalizes blank race_name and zero race_distance_miles."""
    update_data = {
        "date": "2026-05-07",
        "total_distance_miles": 6.2,
        "run_type": "race",
        "environment": "outdoor",
        "race_name": "",
        "race_distance_miles": 0,
        "notes": None,
        "splits": [
            {"split_index": 1, "distance_miles": 1.0, "duration_mmss": "06:00"},
            {"split_index": 2, "distance_miles": 1.0, "duration_mmss": "06:05"},
            {"split_index": 3, "distance_miles": 1.0, "duration_mmss": "05:55"},
            {"split_index": 4, "distance_miles": 3.2, "duration_mmss": "19:00"}
        ]
    }

    mock_session = MagicMock()

    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.splits = [MagicMock()]

    with patch('src.services.run_service.db') as mock_db:
        mock_db.session = mock_session
        with patch('src.services.run_service.RunEntry') as mock_run_class:
            mock_run_class.query.get_or_404.return_value = mock_run
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_split_class.return_value = MagicMock()

                result = RunService.update_run(1, update_data)

                assert result == mock_run
                assert mock_run.race_name is None
                assert mock_run.race_distance_miles is None
                mock_session.commit.assert_called_once()


def test_create_run_database_error():
    """Test run creation fails when commit raises an exception."""
    run_data = {
        "date": "2026-05-07",
        "total_distance_miles": 3.1,
        "run_type": "workout",
        "environment": "treadmill",
        "splits": [
            {"split_index": 1, "distance_miles": 1.0, "duration_mmss": "06:00"},
            {"split_index": 2, "distance_miles": 1.0, "duration_mmss": "06:05"},
            {"split_index": 3, "distance_miles": 1.1, "duration_mmss": "06:40"}
        ]
    }

    mock_session = MagicMock()
    mock_session.commit.side_effect = Exception("Database error")

    with patch('src.services.run_service.db') as mock_db:
        mock_db.session = mock_session
        with patch('src.services.run_service.RunEntry'):
            with pytest.raises(Exception):
                RunService.create_run(run_data)

            mock_session.rollback.assert_called_once()


def test_get_runs_returns_list():
    """Test get_runs returns formatted list."""
    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.date = date(2026, 5, 7)
    mock_run.total_distance_miles = 3.1
    mock_run.run_type = 'workout'
    mock_run.environment = 'treadmill'
    mock_run.race_name = None
    mock_run.race_distance_miles = None
    mock_run.notes = None
    mock_run.created_at = None
    mock_run.updated_at = None

    mock_split = MagicMock()
    mock_split.time_seconds = 360
    mock_split.distance_miles = 1.0
    mock_split.split_index = 1
    mock_run.splits = [mock_split]

    with patch('src.services.run_service.RunEntry') as mock_run_class:
        mock_run_class.query.order_by.return_value.all.return_value = [mock_run]

        result = RunService.get_runs()

        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['summary_pace_seconds_per_mile'] == 360.0
        assert result[0]['split_count'] == 1


def test_get_run_by_id_success():
    """Test get_run_by_id returns formatted run detail."""
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

    mock_split = MagicMock()
    mock_split.split_index = 1
    mock_split.distance_miles = 1.0
    mock_split.time_seconds = 360
    mock_run.splits = [mock_split]

    with patch('src.services.run_service.RunEntry') as mock_run_class:
        mock_run_class.query.get_or_404.return_value = mock_run

        result = RunService.get_run_by_id(1)

        assert result['id'] == 1
        assert result['date'] == '2026-05-07'
        assert len(result['splits']) == 1
        assert result['splits'][0]['pace_seconds_per_mile'] == 360.0


def test_update_run_success():
    """Test successful run update."""
    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.splits = [MagicMock()]

    update_data = {
        "date": "2026-05-08",
        "total_distance_miles": 3.1,
        "run_type": "workout",
        "environment": "outdoor",
        "notes": "Updated run",
        "splits": [{"split_index": 1, "distance_miles": 3.1, "duration_mmss": "19:10"}]
    }

    mock_session = MagicMock()

    with patch('src.services.run_service.db') as mock_db:
        mock_db.session = mock_session
        with patch('src.services.run_service.RunEntry') as mock_run_class:
            mock_run_class.query.get_or_404.return_value = mock_run
            with patch('src.services.run_service.MileSplit') as mock_split_class:
                mock_split_class.return_value = MagicMock()

                result = RunService.update_run(1, update_data)

                assert result == mock_run
                mock_session.commit.assert_called_once()


def test_update_run_validation_error():
    """Test run update with validation error."""
    invalid_data = {
        "total_distance_miles": 3.1,
        "run_type": "workout",
        "environment": "treadmill",
        "splits": []
    }

    with pytest.raises(ValidationError):
        RunService.update_run(1, invalid_data)
