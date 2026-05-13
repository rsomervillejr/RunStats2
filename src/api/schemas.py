from marshmallow import Schema, fields, validates, ValidationError, post_load
from marshmallow.validate import OneOf, Range
import datetime

class BaseSchema(Schema):
    """Base schema with common validation."""
    pass

# Validation constants
VALID_RUN_TYPES = ['race', 'workout']
VALID_ENVIRONMENTS = ['treadmill', 'outdoor']

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
    race_name = fields.Str()
    race_distance_miles = fields.Decimal(places=1)
    notes = fields.Str()
    splits = fields.List(fields.Nested(MileSplitSchema), required=True, validate=lambda x: len(x) > 0)

    @validates('race_name')
    def validate_race_name(self, value):
        if self.context.get('run_type') == 'race' and not value:
            raise ValidationError('race_name is required when run_type is race')

    @validates('race_distance_miles')
    def validate_race_distance(self, value):
        if self.context.get('run_type') == 'race' and not value:
            raise ValidationError('race_distance_miles is required when run_type is race')

    @validates_schema
    def validate_split_distances(self, data, **kwargs):
        """Validate that split distances sum to total distance."""
        if 'splits' in data and 'total_distance_miles' in data:
            total_split_distance = sum(float(split['distance_miles']) for split in data['splits'])
            total_distance = float(data['total_distance_miles'])
            if abs(total_split_distance - total_distance) > 0.001:
                raise ValidationError(
                    f'Split distances sum to {total_split_distance:.3f} miles, '
                    f'but total_distance_miles is {total_distance:.3f}',
                    field_name='splits'
                )

    @post_load
    def set_context(self, data, **kwargs):
        # Set context for field validators
        self.context = data
        return data

class RunEntryResponseSchema(BaseSchema):
    """Schema for run entry responses."""
    id = fields.Int()
    date = fields.Date()
    total_distance_miles = fields.Decimal(places=3)
    run_type = fields.Str()
    environment = fields.Str()
    race_name = fields.Str()
    race_distance_miles = fields.Decimal(places=1)
    notes = fields.Str()
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
    race_name = fields.Str()
    race_distance_miles = fields.Decimal(places=1)
    summary_pace_seconds_per_mile = fields.Decimal(places=3)
    split_count = fields.Int()