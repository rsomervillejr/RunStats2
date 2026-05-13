import os
from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern for Flask app."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    from src.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from src.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Frontend routes
    @app.route('/')
    def view_runs():
        return render_template('view.html')

    @app.route('/edit')
    def edit_run():
        return render_template('edit.html')

    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500

    return app