#Authentication-related routes (includes login, logout, registration)
#Authentication-related routes (includes login, logout, registration)
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
#from app import db
from app.models  import db, User

auth_routes = Blueprint('auth_routes', __name__, template_folder='/templates/auth')


# Registration Route
# Registration Route
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Role is always set to 'student' for new users
        role = 'student'

        # Validate form data
        if not all([first_name, last_name, username, email, password]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth_routes.register'))

        # Check if username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('auth_routes.register'))

        # Hash the password and create a new student user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('auth_routes.login'))

    return render_template('auth/register.html')  # Registration form



#Login Route
# Login Route
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate form data
        if not all([username, password]):
            flash('Username and Password are required.', 'danger')
            return redirect(url_for('auth_routes.login'))

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        # Check if user exists and if the password matches
        if user and check_password_hash(user.password, password):
            # Store user data in the session
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role

            # Redirect based on user role
            if user.role == 'admin':
                return redirect(url_for('admin_routes.admin_dashboard'))  # Redirect for admin
            elif user.role == 'teacher':
                return redirect(url_for('teacher.dashboard'))  # Redirect for teacher
            elif user.role == 'student':
                return redirect(url_for('admin_routes.admin_dashboard'))  # Redirect for student (temporary set to admin to test to see if it works)
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth_routes.login'))

    return render_template('auth/login.html')  # Login form


#Logout Route 
@auth_routes.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()

    # Flash a message to notify the user of successful logout
    flash('You have been logged out successfully.', 'success')

    # Redirect to the login page
    return redirect(url_for('auth_routes.login'))


