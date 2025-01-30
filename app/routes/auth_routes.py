from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Student, db, User
from flask_login import login_user, logout_user, login_required

auth_routes = Blueprint('auth_routes', __name__, template_folder='/templates/auth')

# Registration Route
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        grade = request.form.get('grade')  # New field for grade

        # Role is always set to 'student' for new users
        role = 'student'

        # Validate form data
        if not all([first_name, last_name, username, email, password, grade]):
            flash('All fields, including grade, are required.', 'danger')
            return render_template('auth/register.html', 
                                   first_name=first_name, 
                                   last_name=last_name, 
                                   username=username, 
                                   email=email,
                                   grade=grade)

        # Ensure grade is a valid number
        if not grade.isdigit() or int(grade) not in range(1, 5):  
            flash('Grade must be a valid number.', 'danger')
            return render_template('auth/register.html', 
                                   first_name=first_name, 
                                   last_name=last_name, 
                                   username=username, 
                                   email=email,
                                   grade=grade)

        # Check password length
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('auth/register.html', 
                                   first_name=first_name, 
                                   last_name=last_name, 
                                   username=username, 
                                   email=email,
                                   grade=grade)

        # Check if username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already exists.', 'danger')
            return render_template('auth/register.html', 
                                   first_name=first_name, 
                                   last_name=last_name, 
                                   username=username, 
                                   email=email,
                                   grade=grade)

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

        try:
            db.session.add(new_user)
            db.session.flush()  # Get the user ID before committing to use it in Student model

            # Add grade information to the Student table
            new_student = Student(user_id=new_user.user_id, grade_level=str(grade))
            db.session.add(new_student)
            db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('auth_routes.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            return render_template('auth/register.html', 
                                   first_name=first_name, 
                                   last_name=last_name, 
                                   username=username, 
                                   email=email,
                                   grade=grade)

    return render_template('auth/register.html')

# Login Route
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('You have successfully logged in!', 'success')

        # Check the user's role and redirect accordingly
            if user.role == 'teacher':  # Assuming you have 'teacher' and 'student' roles
                return redirect(url_for('teacher.teacher_dashboard'))  # Replace with your teacher dashboard route
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))  # Replace with your student dashboard route
            else:
                return redirect(url_for('landing.home'))

            # Handle redirection after login
            next_page = request.args.get('next')
            return redirect(next_page or url_for('landing_routes.home'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('auth/login.html')

# Teacher Dashboard Route
@auth_routes.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    # Ensure the user is a teacher before showing the dashboard
    if current_user.role != 'teacher':
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('auth_routes.login'))

    # Your teacher dashboard logic here
    return render_template('teacher/teacher_dashboard.html')


# Logout Route
@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()  # Use Flask-Login's logout_user for session cleanup
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth/logout.html'))
