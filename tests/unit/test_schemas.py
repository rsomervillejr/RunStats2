import pytest
from marshmallow import ValidationError
from src.schemas import MileSplitRequestSchema


class TestMileSplitRequestSchema:
    def test_loads_duration_mmss_into_time_seconds(self):
        schema = MileSplitRequestSchema()
        result = schema.load({
            "split_index": 1,
            "distance_miles": 1.0,
            "duration_mmss": "06:00"
        })

        assert result["split_index"] == 1
        assert float(result["distance_miles"]) == 1.0
        assert result["time_seconds"] == 360
        assert "duration_mmss" not in result

    @pytest.mark.parametrize(
        "invalid_duration",
        ["6:00", "5:3", "5:03", "05:3", "60:00", "00:60", "abc", "", "  "]
    )
    def test_invalid_duration_mmss_formats_raise_validation_error(self, invalid_duration):
        schema = MileSplitRequestSchema()

        with pytest.raises(ValidationError):
            schema.load({
                "split_index": 1,
                "distance_miles": 1.0,
                "duration_mmss": invalid_duration
            })

    def test_zero_duration_mmss_is_rejected(self):
        schema = MileSplitRequestSchema()

        with pytest.raises(ValidationError):
            schema.load({
                "split_index": 1,
                "distance_miles": 1.0,
                "duration_mmss": "00:00"
            })
