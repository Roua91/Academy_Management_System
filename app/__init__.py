'''
Purpose: 
1) Initializes the Flask app. 
2) Sets up configurations, 
3) database connections and extensions like Flask-Migrate or Flask-Login.
4) Registers blueprints for modular routes.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Set up app configurations
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Path to the SQLite database

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (if any)
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app
