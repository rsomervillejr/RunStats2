import pytest
from datetime import date
from src.models import RunEntry, MileSplit, db

class TestRunEntryModel:
    """Unit tests for RunEntry model."""

    def test_run_entry_creation(self):
        """Test basic RunEntry creation."""
        run = RunEntry(
            date=date(2026, 5, 7),
            total_distance_miles=6.2,
            run_type='race',
            environment='outdoor',
            race_name='City 10K',
            race_distance_miles=6.2
        )
        assert run.date == date(2026, 5, 7)
        assert run.total_distance_miles == 6.2
        assert run.run_type == 'race'
        assert run.environment == 'outdoor'
        assert run.race_name == 'City 10K'
        assert run.race_distance_miles == 6.2

    def test_run_entry_requires_date(self):
        """Test RunEntry date column is non-nullable."""
        assert RunEntry.__table__.c.date.nullable is False

    def test_run_entry_requires_total_distance(self):
        """Test RunEntry total_distance_miles column is non-nullable."""
        assert RunEntry.__table__.c.total_distance_miles.nullable is False

    def test_run_entry_requires_run_type(self):
        """Test RunEntry run_type column is non-nullable."""
        assert RunEntry.__table__.c.run_type.nullable is False

    def test_run_entry_requires_environment(self):
        """Test RunEntry environment column is non-nullable."""
        assert RunEntry.__table__.c.environment.nullable is False

    def test_run_entry_race_fields_optional_for_workout(self):
        """Test race fields are optional for workout runs."""
        run = RunEntry(
            date=date(2026, 5, 7),
            total_distance_miles=3.1,
            run_type='workout',
            environment='treadmill'
        )
        assert run.run_type == 'workout'
        assert run.race_name is None
        assert run.race_distance_miles is None

class TestMileSplitModel:
    """Unit tests for MileSplit model."""

    def test_mile_split_creation(self):
        """Test basic MileSplit creation."""
        split = MileSplit(
            run_id=1,
            split_index=1,
            distance_miles=1.0,
            time_seconds=360
        )
        assert split.run_id == 1
        assert split.split_index == 1
        assert split.distance_miles == 1.0
        assert split.time_seconds == 360

    def test_mile_split_requires_run_id(self):
        """Test MileSplit run_id column is non-nullable."""
        assert MileSplit.__table__.c.run_id.nullable is False

    def test_mile_split_requires_split_index(self):
        """Test MileSplit split_index column is non-nullable."""
        assert MileSplit.__table__.c.split_index.nullable is False

    def test_mile_split_requires_distance(self):
        """Test MileSplit distance_miles column is non-nullable."""
        assert MileSplit.__table__.c.distance_miles.nullable is False

    def test_mile_split_requires_time(self):
        """Test MileSplit time_seconds column is non-nullable."""
        assert MileSplit.__table__.c.time_seconds.nullable is False