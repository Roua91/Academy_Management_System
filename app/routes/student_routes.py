from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import db  # Correct import for db
from app.models import Attendance, Course, Student, Enrollment, Grade

# Create the student blueprint
student_routes = Blueprint('student_routes', __name__, template_folder='templates/student')

# Student Dashboard Route
@student_routes.route('/dashboard')
def dashboard():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    # Render the student dashboard
    return render_template('student/student_dashboard.html', username=session.get('username'))


# Route for course enrollment

@student_routes.route('/enroll', methods=['GET', 'POST'])
def enroll():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    student_id = session.get('user_id')

    # Query available courses from the database
    courses = Course.query.all()

    if request.method == 'POST':
        # Get the selected course_id from the form
        selected_course_id = request.form.get('course_id')

        # Ensure the course exists and the student is not already enrolled
        if selected_course_id:
            existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=selected_course_id).first()
            if existing_enrollment:
                flash("You are already enrolled in this course.", "warning")
            else:
                # Enroll the student in the selected course
                enrollment = Enrollment(student_id=student_id, course_id=selected_course_id)
                db.session.add(enrollment)
                db.session.commit()
                flash("Successfully enrolled in the course!", "success")
                return redirect(url_for('student_routes.dashboard'))

    return render_template('student/enroll.html', courses=courses)




# Route to view attendance
@student_routes.route('/attendance')
def view_attendance():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    student_id = session.get('user_id')
    student = Student.query.filter_by(user_id=student_id).first()

    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('auth_routes.login'))

    attendance_records = (
        db.session.query(Attendance, Course)
        .join(Course, Attendance.course_id == Course.course_id)
        .filter(Attendance.student_id == student.student_id)
        .all()
    )

    if not attendance_records:
        flash("No attendance records found.", "info")

    return render_template('student/attendance.html', attendance=attendance_records)


# Route to view grades
@student_routes.route('/grades')
def view_grades():
    # Check if the user is logged in and is a student
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('auth_routes.login'))

    student_id = session.get('user_id')
    student = Student.query.filter_by(user_id=student_id).first()

    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('auth_routes.login'))

    grades_records = (
        db.session.query(Grade, Course)
        .join(Course, Grade.course_id == Course.course_id)
        .filter(Grade.student_id == student.student_id)
        .all()
    )

    if not grades_records:
        flash("No grades found.", "info")

    return render_template('student/grades.html', grades=grades_records)
