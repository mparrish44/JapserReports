import sqlite3

# Step 1: Create/connect to database file
conn = sqlite3.connect("student_mgmt.db")
cursor = conn.cursor()

# Step 2: Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    email TEXT,
    gender TEXT CHECK(gender IN ('M', 'F', 'Other')),
    enrollment_date TEXT
);

CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    course_code TEXT,
    credit_hours INTEGER
);

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date TEXT,
    grade TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE IF NOT EXISTS instructors (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    hire_date TEXT
);

CREATE TABLE IF NOT EXISTS course_assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    instructor_id INTEGER,
    semester TEXT,
    year INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
);
""")

conn.commit()
conn.close()

print("SQLite database and all tables have been created successfully.")
