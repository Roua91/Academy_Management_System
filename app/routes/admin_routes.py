from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, User, Student, Teacher, Course
from sqlalchemy.exc import IntegrityError

# Define the Blueprint for admin routes
admin_routes = Blueprint('admin_routes', __name__)

# ------------------------------
# Admin Dashboard
# ------------------------------
@admin_routes.route('/dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')


# ------------------------------
# Students Management
# ------------------------------
@admin_routes.route('/students')
def students_management():
    try:
        students = db.session.query(Student, User).join(User, Student.user_id == User.user_id).all()
        return render_template('admin/students_man.html', students=students)
    except Exception as e:
        print(f"Error fetching students: {e}")
        flash("Error loading Students Management Page.", "error")


@admin_routes.route('/students/add', methods=['POST'])
def add_student():
    try:
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        grade_level = request.form.get('grade_level')

        # Validate form data
        if not first_name or not last_name or not grade_level:
            flash("All fields are required to add a student.", "error")
            return redirect(url_for('admin_routes.students_management'))

        # Add user and student records
        user = User(first_name=first_name, last_name=last_name, role='student')
        db.session.add(user)
        db.session.flush()  # Get user_id after insertion

        student = Student(user_id=user.user_id, grade_level=grade_level)
        db.session.add(student)
        db.session.commit()

        flash('Student added successfully!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error adding student. Please try again.', 'error')
    except Exception as e:
        db.session.rollback()
        print(f"Error adding student: {e}")
        flash('Unexpected error occurred. Please try again.', 'error')

    return redirect(url_for('admin_routes.students_management'))


@admin_routes.route('/students/update/<int:student_id>', methods=['POST'])
def update_student(student_id):
    try:
        # Fetch the student record
        student = db.session.query(Student, User).join(User, Student.user_id == User.user_id).filter(
            Student.student_id == student_id).first()

        if not student:
            flash("Student not found.", "error")
            return redirect(url_for('admin_routes.students_management'))

        # Update student and user fields
        student.User.first_name = request.form.get('first_name')
        student.User.last_name = request.form.get('last_name')
        student.Student.grade_level = request.form.get('grade_level')

        db.session.commit()
        flash('Student updated successfully!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error updating student. Please try again.', 'error')
    except Exception as e:
        db.session.rollback()
        print(f"Error updating student: {e}")
        flash('Unexpected error occurred. Please try again.', 'error')

    return redirect(url_for('admin_routes.students_management'))


@admin_routes.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        # Fetch the student record
        student = Student.query.get(student_id)
        if not student:
            flash("Student not found.", "error")
            return redirect(url_for('admin_routes.students_management'))

        # Delete student and associated user
        db.session.delete(student)
        db.session.delete(User.query.get(student.user_id))
        db.session.commit()

        flash('Student deleted successfully!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error deleting student. Please try again.', 'error')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting student: {e}")
        flash('Unexpected error occurred. Please try again.', 'error')

    return redirect(url_for('admin_routes.students_management'))


# ------------------------------
# Teachers Management
# ------------------------------
@admin_routes.route('/teachers')
def teachers_management():
    teachers = db.session.query(Teacher, User).join(User, Teacher.user_id == User.user_id).all()
    return render_template('admin/teachers_man.html', teachers=teachers)


@admin_routes.route('/teachers/add', methods=['POST'])
def add_teacher():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')  # Hash this in production
    specialization = request.form.get('specialization')
    hire_date = request.form.get('hire_date')

    # Create User and Teacher
    user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, role='teacher')
    db.session.add(user)
    db.session.flush()  # Get user_id for the teacher

    teacher = Teacher(user_id=user.user_id, specialization=specialization, hire_date=hire_date)
    db.session.add(teacher)

    try:
        db.session.commit()
        flash('Teacher added successfully!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error adding teacher. Please try again.', 'error')

    return redirect(url_for('admin_routes.teachers_management'))


@admin_routes.route('/teachers/update/<int:teacher_id>', methods=['GET', 'POST'])
def update_teacher(teacher_id):
    teacher = db.session.query(Teacher, User).join(User, Teacher.user_id == User.user_id).filter(Teacher.teacher_id == teacher_id).first()

    if request.method == 'POST':
        teacher.User.first_name = request.form.get('first_name')
        teacher.User.last_name = request.form.get('last_name')
        teacher.Teacher.specialization = request.form.get('specialization')

        try:
            db.session.commit()
            flash('Teacher updated successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error updating teacher. Please try again.', 'error')

        return redirect(url_for('admin_routes.teachers_management'))

    return render_template('update_teacher.html', teacher=teacher)


@admin_routes.route('/teachers/delete/<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if teacher:
        db.session.delete(teacher)
        db.session.delete(User.query.get(teacher.user_id))
        try:
            db.session.commit()
            flash('Teacher deleted successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error deleting teacher. Please try again.', 'error')

    return redirect(url_for('admin_routes.teachers_management'))


# ------------------------------
# Courses Management
# ------------------------------
@admin_routes.route('/courses', methods=['GET'])
def courses_management():
    try:
        # Fetch courses and join them with teachers and their users
        courses = db.session.query(Course, Teacher).join(Teacher, Course.teacher_id == Teacher.teacher_id).all()

        # Fetch teachers and ensure their user relationship is loaded
        teachers = Teacher.query.options(db.joinedload(Teacher.user)).all()

        return render_template('admin/courses_man.html', courses=courses, teachers=teachers)
    except Exception as e:
        print(f"Error fetching courses: {e}")
        return "Error loading Courses Management Page", 500


@admin_routes.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        grade_level = request.form.get('grade_level')
        teacher_id = request.form.get('teacher_id')

        course = Course(course_name=course_name, grade_level=grade_level, teacher_id=teacher_id)
        db.session.add(course)

        try:
            db.session.commit()
            flash('Course added successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error adding course. Please try again.', 'error')

        return redirect(url_for('admin_routes.courses_management'))

    teachers = Teacher.query.all()
    return render_template('add_course.html', teachers=teachers)


@admin_routes.route('/courses/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        try:
            db.session.commit()
            flash('Course deleted successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error deleting course. Please try again.', 'error')

    return redirect(url_for('admin_routes.courses_management'))