from app import create_app
from app.models import db

app = create_app()

# Debugging app and database
print(f"App: {app}")
print(f"SQLAlchemy Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

with app.app_context():
    db.create_all()
    print("Database initialized successfully!")
