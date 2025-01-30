"""
Purpose:
1) Initializes the Flask app.
2) Sets up configurations.
3) Configures database connections and extensions like Flask-Migrate or Flask-Login.
4) Registers blueprints for modular routes.
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth_routes.login'  # The login route for redirection if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    
    # Define the user_loader function to load a user from the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Query user by their ID (ensure 'user_id' is your primary key)

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
    from app.routes.auth_routes import auth_routes
    from app.routes.student_routes import student_routes
    from app.routes.teacher_routes import teacher_routes
    from app.routes.landing import landing_routes
    app.register_blueprint(admin_routes, url_prefix='/admin')
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(student_routes, url_prefix='/student')
    app.register_blueprint(landing_routes)
    app.register_blueprint(teacher_routes, url_prefix='/teacher')


    return app