from src.models import db
from datetime import datetime

class MileSplit(db.Model):
    """Model for mile splits within a run."""
    __tablename__ = 'mile_splits'

    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('run_entries.id'), nullable=False)
    split_index = db.Column(db.Integer, nullable=False)
    distance_miles = db.Column(db.Numeric(5, 3), nullable=False)
    time_seconds = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint on (run_id, split_index)
    __table_args__ = (
        db.UniqueConstraint('run_id', 'split_index', name='unique_run_split_index'),
    )

    def __repr__(self):
        return f'<MileSplit {self.id}: Run {self.run_id} Split {self.split_index}>'