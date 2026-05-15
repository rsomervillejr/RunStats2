from marshmallow import Schema, fields, validates, validates_schema, ValidationError, post_load, pre_load
from marshmallow.validate import OneOf, Range, Regexp
import datetime

class BaseSchema(Schema):
    """Base schema with common validation."""
    pass

# Validation constants
VALID_RUN_TYPES = ['race', 'workout']
VALID_ENVIRONMENTS = ['treadmill', 'outdoor']

class MileSplitRequestSchema(BaseSchema):
    """Schema for mile split request data."""
    split_index = fields.Int(required=True, validate=Range(min=1))
    distance_miles = fields.Decimal(required=True, places=3, validate=Range(min=0.001))
    duration_mmss = fields.Str(
        required=True,
        load_only=True,
        validate=Regexp(r'^[0-5][0-9]:[0-5][0-9]$', error='duration_mmss must be mm:ss with minutes and seconds 00-59')
    )
    time_seconds = fields.Int(load_only=True, required=False, validate=Range(min=1))

    @pre_load
    def convert_duration_mmss(self, data, **kwargs):
        if not isinstance(data, dict):
            return data

        duration = data.get('duration_mmss')
        if duration is not None:
            try:
                duration = str(duration).strip()
                minutes, seconds = duration.split(':')
                total_seconds = int(minutes) * 60 + int(seconds)
            except (ValueError, AttributeError):
                return data

            if total_seconds == 0:
                raise ValidationError('duration_mmss must be greater than 00:00', field_name='duration_mmss')

            data['time_seconds'] = total_seconds

        return data

    @post_load
    def remove_duration_mmss(self, data, **kwargs):
        data.pop('duration_mmss', None)
        return data

class MileSplitSchema(BaseSchema):
    """Schema for mile split data."""
    split_index = fields.Int(required=True, validate=Range(min=1))
    distance_miles = fields.Decimal(required=True, places=3, validate=Range(min=0.001))
    time_seconds = fields.Int(required=True, validate=Range(min=1))

class RunEntrySchema(BaseSchema):
    """Schema for run entry creation/update."""
    date = fields.Date(required=True)
    total_distance_miles = fields.Decimal(required=True, places=3, validate=Range(min=0.001))
    run_type = fields.Str(required=True, validate=OneOf(VALID_RUN_TYPES))
    environment = fields.Str(required=True, validate=OneOf(VALID_ENVIRONMENTS))
    race_name = fields.Str(allow_none=True)
    race_distance_miles = fields.Decimal(places=1, allow_none=True, validate=Range(min=0.001))
    notes = fields.Str(allow_none=True)
    splits = fields.List(fields.Nested(MileSplitRequestSchema), required=True, validate=lambda x: len(x) > 0)

    @pre_load
    def normalize_nullable_race_fields(self, data, **kwargs):
        if not isinstance(data, dict):
            return data

        if 'race_name' in data and data.get('race_name') is not None:
            race_name = str(data.get('race_name')).strip()
            if race_name == '':
                data['race_name'] = None

        if 'race_distance_miles' in data and data.get('race_distance_miles') is not None:
            try:
                distance_value = float(data.get('race_distance_miles'))
                if distance_value == 0:
                    data['race_distance_miles'] = None
            except (TypeError, ValueError):
                pass

        return data

    @validates_schema
    def validate_race_and_split_distances(self, data, **kwargs):
        race_name = data.get('race_name')
        if race_name is not None and not str(race_name).strip():
            raise ValidationError('race_name cannot be blank', field_name='race_name')

        if 'splits' in data and 'total_distance_miles' in data:
            total_split_distance = sum(float(split['distance_miles']) for split in data['splits'])
            total_distance = float(data['total_distance_miles'])
            if abs(total_split_distance - total_distance) > 0.001:
                raise ValidationError(
                    f'Split distances sum to {total_split_distance:.3f} miles, '
                    f'but total_distance_miles is {total_distance:.3f}',
                    field_name='splits'
                )

class RunEntryResponseSchema(BaseSchema):
    """Schema for run entry responses."""
    id = fields.Int()
    date = fields.Date()
    total_distance_miles = fields.Decimal(places=3)
    run_type = fields.Str()
    environment = fields.Str()
    race_name = fields.Str(allow_none=True)
    race_distance_miles = fields.Decimal(places=1, allow_none=True)
    notes = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    splits = fields.List(fields.Nested(MileSplitSchema()))

class RunListResponseSchema(BaseSchema):
    """Schema for run list responses."""
    id = fields.Int()
    date = fields.Date()
    total_distance_miles = fields.Decimal(places=3)
    run_type = fields.Str()
    environment = fields.Str()
    race_name = fields.Str(allow_none=True)
    race_distance_miles = fields.Decimal(places=1, allow_none=True)
    summary_pace_seconds_per_mile = fields.Decimal(places=3)
    split_count = fields.Int()
