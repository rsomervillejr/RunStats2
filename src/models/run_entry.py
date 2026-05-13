from src.models import db
from datetime import datetime

class RunEntry(db.Model):
    """Model for run entries."""
    __tablename__ = 'run_entries'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total_distance_miles = db.Column(db.Numeric(6, 3), nullable=False)
    run_type = db.Column(db.String(20), nullable=False)  # 'race' or 'workout'
    environment = db.Column(db.String(20), nullable=False)  # 'treadmill' or 'outdoor'
    race_name = db.Column(db.String(200))
    race_distance_miles = db.Column(db.Numeric(5, 1))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to splits
    splits = db.relationship('MileSplit', backref='run', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<RunEntry {self.id}: {self.date} {self.total_distance_miles}mi>'