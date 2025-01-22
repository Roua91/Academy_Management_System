from flask import Blueprint, render_template

# Blueprint for the landing page and related routes
landing_routes = Blueprint('landing_routes', __name__, template_folder='/templates/landing')

@landing_routes.route('/')
def home():
    return render_template('landing/landing.html')
