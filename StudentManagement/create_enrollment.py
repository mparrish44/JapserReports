import sqlite3
from faker import Faker
import random
from datetime import datetime

# Connect to the existing database
conn = sqlite3.connect("student_mgmt.db")
cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Populate 'courses' table
course_names = ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
                "History", "Geography", "English", "Art", "Music", "Economics", "Psychology"]
courses = [(name, f"{name[:4].upper()}{random.randint(100,499)}", random.randint(2,5)) for name in course_names]

cursor.executemany("""
    INSERT INTO courses (course_name, course_code, credit_hours)
    VALUES (?, ?, ?);
""", courses)

# Populate 'instructors' table
instructors = [(fake.first_name(), fake.last_name(), fake.email(), fake.date_between(start_date='-10y', end_date='today').isoformat()) for _ in range(100)]
cursor.executemany("""
    INSERT INTO instructors (first_name, last_name, email, hire_date)
    VALUES (?, ?, ?, ?);
""", instructors)

# Get all student and course IDs
cursor.execute("SELECT student_id FROM students")
student_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT course_id FROM courses")
course_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT instructor_id FROM instructors")
instructor_ids = [row[0] for row in cursor.fetchall()]

# Populate 'enrollments' table
enrollments = []
for student_id in student_ids:
    for course_id in random.sample(course_ids, k=random.randint(2, 5)):
        enrollments.append((
            student_id,
            course_id,
            fake.date_between(start_date='-3y', end_date='today').isoformat(),
            random.choice(['A', 'B', 'C', 'D', 'F'])
        ))

cursor.executemany("""
    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (?, ?, ?, ?);
""", enrollments)

# Populate 'course_assignments' table
assignments = []
for course_id in course_ids:
    for _ in range(random.randint(1, 2)):  # Each course taught by 1-2 instructors
        assignments.append((
            course_id,
            random.choice(instructor_ids),
            random.choice(['Fall', 'Spring']),
            random.randint(2020, 2025)
        ))

cursor.executemany("""
    INSERT INTO course_assignments (course_id, instructor_id, semester, year)
    VALUES (?, ?, ?, ?);
""", assignments)

# Commit and close
conn.commit()
conn.close()

"Database population complete: courses, instructors, enrollments, and course_assignments filled."
