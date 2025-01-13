from flask import Blueprint

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    return "Welcome to the Academy Management System!"
