# Define Database Schema
from flask_sqlalchemy import SQLAlchemy
from app import db
from flask_login import UserMixin

# Base User model

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # student, teacher, admin

    # Relationship to Teacher
    teacher_relationship = db.relationship('Teacher', backref='teacher_user', uselist=False)

    # Relationship to Student
    student_relationship = db.relationship('Student', backref='student_user', uselist=False)

    # Flask-Login requires this method
    def get_id(self):
        return str(self.user_id)


# Students model
class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    grade_level = db.Column(db.String(5), nullable=False)

    # No need to redefine `user` as it's accessible via the `backref`
    @property
    def first_name(self):
        return self.student_user.first_name  # Use the backref

    @property
    def last_name(self):
        return self.student_user.last_name


# Teachers model
class Teacher(db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)

    # No need to redefine `user` as it's accessible via the `backref`
    @property
    def first_name(self):
        return self.teacher_user.first_name  # Use the backref

    @property
    def last_name(self):
        return self.teacher_user.last_name

    
# Admins model
class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    office_location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)

# Courses model
class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.String(5), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)

# Enrollments model
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

# Attendance model
class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # Present, Absent, Late
    # Define the relationship to the Student model
    student = db.relationship('Student', backref='attendances')

# Grades model
class Grade(db.Model):
    __tablename__ = 'grades'
    grade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    assignment_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    #grade = db.Column(db.Float, nullable=False)
    submission_date = db.Column(db.Date, nullable=True)
