# Student module routes
from flask import Blueprint, render_template, session, redirect, url_for, flash

# Create the student blueprint
student_routes = Blueprint('student_routes', __name__, template_folder='/templates/student')

# Student Dashboard Route
@student_routes.route('/dashboard')
def dashboard():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    # Render the student dashboard
    return render_template('student/student_dashboard.html', username=session.get('username'))

