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



# view grades
from sqlalchemy.sql import text  # Import text explicitly

@student_routes.route('/grades', methods=['GET'])
def view_grades():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    # Fetch grades for the logged-in student
    student_id = session.get('user_id')  # Assuming user_id corresponds to the student's ID
    grades_query = text("""
        SELECT c.course_name, g.grade
        FROM grades g
        JOIN courses c ON g.course_id = c.course_id
        WHERE g.student_id = :student_id
    """)
    grades = db.session.execute(grades_query, {'student_id': student_id}).fetchall()

    # Render the grades page
    return render_template('student/grades.html', grades=grades)

    # view attendance
    from sqlalchemy.sql import text  # Import text for raw SQL queries

@student_routes.route('/attendance', methods=['GET'])
def view_attendance():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    # Fetch attendance data for the logged-in student
    student_id = session.get('user_id')  # Assuming user_id corresponds to the student's ID
    try:
        attendance_query = text("""
            SELECT c.course_name,
                   SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.status) AS attendance_percentage
            FROM attendance a
            JOIN courses c ON a.course_id = c.course_id
            WHERE a.student_id = :student_id
            GROUP BY c.course_name
        """)
        attendance_data = db.session.execute(attendance_query, {'student_id': student_id}).fetchall()
    except Exception as e:
        # Handle errors if the query fails
        flash(f"An error occurred while fetching attendance data: {str(e)}", 'danger')
        return redirect(url_for('student_routes.dashboard'))

    # Render the attendance page with the fetched data
    return render_template('student/attendance.html', attendance_data=attendance_data)



# enroll
@student_routes.route('/enroll', methods=['GET', 'POST'])
def enroll():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    # Fetch all courses
    courses = Course.query.all()

    if request.method == 'POST':
        selected_course_id = request.form.get('course')  # Course ID from the form

        # Make sure a course was selected
        if selected_course_id:
            # Logic for enrolling the student in a course
            flash('You have successfully enrolled in the course!', 'success')
            return redirect(url_for('student_routes.dashboard'))
        else:
            flash('Please select a course.', 'danger')

    # Render the enrollment page with available courses
    return render_template('student/enroll.html', courses=courses)

