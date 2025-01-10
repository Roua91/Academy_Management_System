from app import create_app, db

# Create the Flask application instance
app = create_app()

# Run the app when executed directly
if __name__ == '__main__':
    app.run(debug=True)

