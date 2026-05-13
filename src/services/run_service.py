from src.models import db, RunEntry, MileSplit
from src.api.schemas import RunEntrySchema, RunEntryResponseSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

class RunService:
    """Service layer for run operations."""

    @staticmethod
    def create_run(run_data):
        """Create a new run with splits."""
        try:
            # Validate input data
            schema = RunEntrySchema()
            validated_data = schema.load(run_data)

            # Create run entry
            run = RunEntry(
                date=validated_data['date'],
                total_distance_miles=validated_data['total_distance_miles'],
                run_type=validated_data['run_type'],
                environment=validated_data['environment'],
                race_name=validated_data.get('race_name'),
                race_distance_miles=validated_data.get('race_distance_miles'),
                notes=validated_data.get('notes')
            )

            # Create splits
            for split_data in validated_data['splits']:
                split = MileSplit(
                    split_index=split_data['split_index'],
                    distance_miles=split_data['distance_miles'],
                    time_seconds=split_data['time_seconds']
                )
                run.splits.append(split)

            # Save to database
            db.session.add(run)
            db.session.commit()

    @staticmethod
    def update_run(run_id, run_data):
        """Update an existing run with splits."""
        try:
            # Get existing run
            run = RunEntry.query.get_or_404(run_id)

            # Validate input data
            schema = RunEntrySchema()
            validated_data = schema.load(run_data)

            # Update run entry
            run.date = validated_data['date']
            run.total_distance_miles = validated_data['total_distance_miles']
            run.run_type = validated_data['run_type']
            run.environment = validated_data['environment']
            run.race_name = validated_data.get('race_name')
            run.race_distance_miles = validated_data.get('race_distance_miles')
            run.notes = validated_data.get('notes')

            # Replace splits - delete existing and create new ones
            for split in run.splits:
                db.session.delete(split)

            run.splits = []
            for split_data in validated_data['splits']:
                split = MileSplit(
                    split_index=split_data['split_index'],
                    distance_miles=split_data['distance_miles'],
                    time_seconds=split_data['time_seconds']
                )
                run.splits.append(split)

            # Save to database
            db.session.commit()

            logger.info(f"Updated run {run.id} with {len(run.splits)} splits")
            return run

        except ValidationError as e:
            logger.error(f"Validation error updating run {run_id}: {e.messages}")
            raise
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Database integrity error updating run {run_id}: {e}")
            raise
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected error updating run {run_id}: {e}")
            raise

    @staticmethod
    def get_runs():
        """Get all runs ordered by date descending."""
        runs = RunEntry.query.order_by(RunEntry.date.desc()).all()

        # Add computed fields for list view
        result = []
        for run in runs:
            # Calculate summary pace (simple average for now)
            if run.splits:
                total_time = sum(split.time_seconds for split in run.splits)
                total_distance = sum(float(split.distance_miles) for split in run.splits)
                summary_pace = total_time / total_distance if total_distance > 0 else 0
            else:
                summary_pace = 0

            result.append({
                'id': run.id,
                'date': run.date,
                'total_distance_miles': run.total_distance_miles,
                'run_type': run.run_type,
                'environment': run.environment,
                'race_name': run.race_name,
                'race_distance_miles': run.race_distance_miles,
                'summary_pace_seconds_per_mile': round(summary_pace, 3),
                'split_count': len(run.splits)
            })

        return result

    @staticmethod
    def get_run_by_id(run_id):
        """Get a specific run with splits."""
        run = RunEntry.query.get_or_404(run_id)

        # Calculate pace for each split
        splits_data = []
        for split in sorted(run.splits, key=lambda s: s.split_index):
            pace = split.time_seconds / float(split.distance_miles) if split.distance_miles > 0 else 0
            splits_data.append({
                'split_index': split.split_index,
                'distance_miles': split.distance_miles,
                'time_seconds': split.time_seconds,
                'pace_seconds_per_mile': round(pace, 3)
            })

        return {
            'id': run.id,
            'date': run.date,
            'total_distance_miles': run.total_distance_miles,
            'run_type': run.run_type,
            'environment': run.environment,
            'race_name': run.race_name,
            'race_distance_miles': run.race_distance_miles,
            'notes': run.notes,
            'created_at': run.created_at,
            'updated_at': run.updated_at,
            'splits': splits_data
        }