'''
Purpose: 
1) Initializes the Flask app. 
2) Sets up configurations, 
3) database connections and extensions like Flask-Migrate or Flask-Login.
4) Registers blueprints for modular routes.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Configuration for the application
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'academy.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

    # Initialize the database with the app directly
    global db
    db.init_app(app)

    # Initialize database tables within the app context
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes.main_routes import main_routes
    app.register_blueprint(main_routes)

    return app
