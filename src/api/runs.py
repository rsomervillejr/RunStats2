from flask import request, jsonify
from src.api import api_bp
from src.services.run_service import RunService
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/runs', methods=['GET'])
def get_runs():
    """Get all runs ordered by date descending."""
    try:
        runs = RunService.get_runs()
        return jsonify(runs)
    except Exception as e:
        logger.error(f"Error getting runs: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/runs', methods=['POST'])
def create_run():
    """Create a new run entry."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        run = RunService.create_run(data)

        # Return the created run with splits
        result = RunService.get_run_by_id(run.id)
        return jsonify(result), 201

    except ValidationError as e:
        logger.warning(f"Validation error: {e.messages}")
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Error creating run: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/runs/<int:run_id>', methods=['PUT'])
def update_run(run_id):
    """Update an existing run entry."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        run = RunService.update_run(run_id, data)

        # Return the updated run with splits
        result = RunService.get_run_by_id(run.id)
        return jsonify(result)

    except ValidationError as e:
        logger.warning(f"Validation error updating run {run_id}: {e.messages}")
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Error updating run {run_id}: {e}")
        return jsonify({'error': 'Run not found or internal server error'}), 404