"""
Purpose:
1) Initializes the Flask app.
2) Sets up configurations.
3) Configures database connections and extensions like Flask-Migrate or Flask-Login.
4) Registers blueprints for modular routes.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Create and configure the app
    app = Flask(__name__)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Application configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'academy.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')

    # Initialize the database with the app
    db.init_app(app)

    # Import models and create tables only if necessary
    with app.app_context():
        from app.models import User, Student, Teacher  # Import your models here
        
        # Check if the database file exists
        db_path = os.path.join(app.instance_path, 'academy.db')
        if not os.path.exists(db_path):  # If the database file does not exist
            db.create_all()  # Create all tables
            print("Database created and tables initialized.")
        else:
            print("Database already exists. Skipping table creation.")

    # Register blueprints
    from app.routes.admin_routes import admin_routes
    app.register_blueprint(admin_routes, url_prefix='/admin')


    return app
