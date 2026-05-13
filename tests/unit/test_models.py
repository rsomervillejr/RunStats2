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
        """Test RunEntry requires date."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            run = RunEntry(
                total_distance_miles=6.2,
                run_type='race',
                environment='outdoor'
            )

    def test_run_entry_requires_total_distance(self):
        """Test RunEntry requires total_distance_miles."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            run = RunEntry(
                date=date(2026, 5, 7),
                run_type='race',
                environment='outdoor'
            )

    def test_run_entry_requires_run_type(self):
        """Test RunEntry requires run_type."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            run = RunEntry(
                date=date(2026, 5, 7),
                total_distance_miles=6.2,
                environment='outdoor'
            )

    def test_run_entry_requires_environment(self):
        """Test RunEntry requires environment."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            run = RunEntry(
                date=date(2026, 5, 7),
                total_distance_miles=6.2,
                run_type='race'
            )

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
        """Test MileSplit requires run_id."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            split = MileSplit(
                split_index=1,
                distance_miles=1.0,
                time_seconds=360
            )

    def test_mile_split_requires_split_index(self):
        """Test MileSplit requires split_index."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            split = MileSplit(
                run_id=1,
                distance_miles=1.0,
                time_seconds=360
            )

    def test_mile_split_requires_distance(self):
        """Test MileSplit requires distance_miles."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            split = MileSplit(
                run_id=1,
                split_index=1,
                time_seconds=360
            )

    def test_mile_split_requires_time(self):
        """Test MileSplit requires time_seconds."""
        with pytest.raises(Exception):  # Should fail due to nullable=False
            split = MileSplit(
                run_id=1,
                split_index=1,
                distance_miles=1.0
            )