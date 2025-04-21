# KD Academy Student Management System

A comprehensive web-based platform built using **Flask**, **SQLite**, **HTML**, and **CSS**, designed to simplify the management of student records, teacher interactions, and administrative operations within KD Academy.

## 📌 Project Overview

KD Academy is a full-featured academic management system that provides separate modules for **students**, **teachers**, and **administrators**, allowing secure and seamless management of attendance, grades, and course enrollments. The application includes secure login/logout functionalities and focuses on user experience and operational efficiency.



## 🛠 Tools & Technologies Used

- **Flask**: Web application framework for routing and backend logic.
- **SQLite**: Lightweight and efficient database system.
- **HTML & CSS**: Frontend structure and styling.
- **GitHub**: Version control and collaborative development.


## 🧩 Modules

### 1. Authentication Module
- Landing Page  
- Register Page  
- Login Page  
- Error Handling for duplicate users and weak passwords
![image](https://github.com/user-attachments/assets/c97eebc3-8548-414a-8de0-c0199cb6d312)


### 2. Admin Module
- Dashboard  
- Student Management (Add, View, Update, Delete)  
- Teacher Management (Add, Modify, Delete)  
- Course Management (Create, Assign teachers)
![image](https://github.com/user-attachments/assets/1b5b299c-65a4-499d-ad88-4c89d8539fa0)


### 3. Teacher Module
- Dashboard  
- Record Attendance  
- View Attendance by Date  
- Grade Assessment  
- View Grades by Assignment  
- Secure Logout
![image](https://github.com/user-attachments/assets/881160cc-17e4-4197-a1e3-3ae223bfe94a)

  

### 4. Student Module
- Dashboard  
- View Attendance  
- View Grades  
- Course Enrollment
  ![image](https://github.com/user-attachments/assets/9c12aef7-9ba2-4403-b69e-ecabc18fb327)


## Key Features

- 👨‍🏫 Multi-role access for Admins, Teachers, and Students
- 🗃️ Organized student and course records
- 🧑‍🏫 Attendance and grading systems
- 🔒 Secure login/logout functionality
- 🎨 Clean user interface with pure CSS styling

## steps to follow to run the app:
   - Clone the repository:
     ```bash
     git clone <repository_url>
     cd flask_project
     ```

   - Create their own virtual environment:
     ```bash
     python -m venv venv
     venv\Scripts\activate on Windows
     ```

   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - run the app:
     ```bash
     python run.py
     ```




