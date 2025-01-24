from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app import db
from app.models import Course, Student, Attendance, Grade, Teacher, Enrollment
from datetime import datetime
from sqlalchemy.orm import joinedload

teacher_routes = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher_routes.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    teacher_name = current_user.username  # Assuming `username` exists in the `User` model
    return render_template('teacher/teacher_dashboard.html', teacher_name=teacher_name)

@teacher_routes.route('/record_attendance', methods=['GET', 'POST'])
@login_required
def record_attendance():
    teacher = current_user.teacher_relationship  # Ensure teacher is logged in
    if not teacher:
        flash('Teacher not found!', 'error')
        return redirect(url_for('teacher.dashboard'))

    # Fetch courses taught by the teacher from the 'courses' table
    courses = Course.query.filter_by(teacher_id=teacher.teacher_id).all()

    if not courses:
        flash('No courses found for this teacher!', 'error')
        return redirect(url_for('teacher.dashboard'))

    # Fetch all students (no course filtering needed), but exclude any with empty names
    students = Student.query.filter(Student.first_name != '', Student.last_name != '').all()

    if not students:
        flash('No students found!', 'error')
        return redirect(url_for('teacher.dashboard'))

    course_id = None  # Initialize course_id to None for GET request

    if request.method == 'POST':
        # Get the course_id entered by the teacher from the form
        course_id = request.form.get('course_id')

        # Validate the course_id (make sure it exists in the database)
        if not course_id:
            flash('Course ID is required!', 'error')
            return redirect(url_for('teacher.record_attendance'))

        # Check if the entered course_id exists in the database
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            flash('Invalid Course ID!', 'error')
            return redirect(url_for('teacher.record_attendance'))

        attendance_data = {}
        for student in request.form:
            if student.startswith("attendance_"):
                student_id = student.split("_")[1]
                status = request.form.get(student)
                attendance_data[student_id] = status

        # Debugging: print attendance data
        print(f"Attendance Data: {attendance_data}")

        # Loop through attendance data and insert it into the database
        for student_id, status in attendance_data.items():
            student_id = int(student_id)

            # Check if attendance already exists for the student and course
            existing_attendance = Attendance.query.filter_by(
                student_id=student_id,
                course_id=course_id,
                date=datetime.today().date()
            ).first()

            if existing_attendance:
                existing_attendance.status = status  # Update attendance status
            else:
                # Create new attendance record
                new_attendance = Attendance(
                    student_id=student_id,
                    course_id=course_id,
                    teacher_id=teacher.teacher_id,
                    date=datetime.today().date(),
                    status=status
                )
                db.session.add(new_attendance)

        db.session.commit()
        flash('Attendance successfully recorded!', 'success')
        return redirect(url_for('teacher.record_attendance'))

    return render_template('teacher/record_attendance.html', students=students, courses=courses, course_id=course_id)



@teacher_routes.route('/view_attendance', methods=['GET', 'POST'])
@login_required
def view_attendance():
    teacher = current_user.teacher_relationship  # Ensure teacher is logged in
    if not teacher:
        flash('Teacher not found!', 'error')
        return redirect(url_for('teacher.teacher_dashboard'))

    # Fetch all courses taught by the teacher
    courses = Course.query.filter_by(teacher_id=teacher.teacher_id).all()

    if not courses:
        flash('No courses found for this teacher!', 'error')
        return redirect(url_for('teacher.teacher_dashboard'))

    attendance_records = None
    selected_date = None

    if request.method == 'POST':
        # Get the selected date from the form
        selected_date = request.form.get('attendance_date')

        if not selected_date:
            flash('Please select a date.', 'error')
            return redirect(url_for('teacher.view_attendance'))

        # Fetch attendance records for the selected date and ensure attendance records exist
        attendance_records = Attendance.query.filter(
            Attendance.course_id.in_([course.course_id for course in courses]),
            Attendance.date == selected_date
        ).all()

        # Filter out records with no student or empty status
        attendance_records = [record for record in attendance_records if record.student and record.status]

    return render_template('teacher/view_attendance.html', 
                           courses=courses, 
                           attendance_records=attendance_records,
                           selected_date=selected_date)


@teacher_routes.route('/grade_assessment', methods=['GET', 'POST'])
@login_required
def grade_assessment():
    teacher = current_user.teacher_relationship  # Ensure teacher is logged in
    if not teacher:
        flash('Teacher not found!', 'error')
        return redirect(url_for('teacher.teacher_dashboard'))

    # Fetch all students
    students = Student.query.all()
    assignment_name = None  # This will hold the entered assignment name

    if request.method == 'POST':
        assignment_name = request.form.get('assignment_name')  # Get the assignment name entered by the teacher

        if assignment_name:
            for student in students:
                grade_key = f"grade_{student.student_id}"
                grade = request.form.get(grade_key)

                if grade:  # If a grade is selected
                    # Fetch courses for the student's grade_level
                    courses = Course.query.filter_by(grade_level=student.grade_level).all()

                    for course in courses:
                        course_id = course.course_id  # Accessing the course_id for the grade assignment

                        # Check if there's an existing grade for the student, course, and assignment
                        existing_grade = Grade.query.filter_by(
                            student_id=student.student_id,
                            course_id=course_id,
                            assignment_name=assignment_name
                        ).first()

                        if existing_grade:
                            existing_grade.grade = grade  # Update the existing grade
                        else:
                            # Create a new grade entry
                            new_grade = Grade(
                                student_id=student.student_id,
                                course_id=course_id,
                                assignment_name=assignment_name,
                                grade=grade,
                                submission_date=datetime.utcnow()
                            )
                            db.session.add(new_grade)

            db.session.commit()  # Save the grades to the database
            flash('Grades saved successfully!', 'success')
            return redirect(url_for('teacher.grade_assessment'))

    return render_template('teacher/grade_assessment.html', students=students, assignment_name=assignment_name)




@teacher_routes.route('/view_grades', methods=['GET', 'POST'])
def view_grades():
    grades = []
    assignment_name = ''
    
    if request.method == 'POST':
        # Get the assignment name from the form
        assignment_name = request.form.get('assignment_name')
        
        # Query the grades filtered by the assignment name
        grades = Grade.query.filter(Grade.assignment_name.ilike(f"%{assignment_name}%")).all()
        
    return render_template('teacher/view_grades.html', grades=grades, assignment_name=assignment_name)




