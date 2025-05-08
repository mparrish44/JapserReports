# Re-import necessary modules after code execution state reset
import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker and DB
fake = Faker()
conn = sqlite3.connect("student_mgmt.db")
cur = conn.cursor()

# Create grade_levels and graduation_years tables
cur.execute("""
CREATE TABLE IF NOT EXISTS grade_levels (
    grade_level_id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade_name TEXT UNIQUE NOT NULL
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS graduation_years (
    graduation_year_id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER UNIQUE NOT NULL
)
""")

# Populate grade_levels
grade_levels = ['9th Grade', '10th Grade', '11th Grade', '12th Grade']
cur.executemany("INSERT OR IGNORE INTO grade_levels (grade_name) VALUES (?)", [(g,) for g in grade_levels])

# Populate graduation_years (2024–2027)
graduation_years = [(y,) for y in range(2024, 2028)]
cur.executemany("INSERT OR IGNORE INTO graduation_years (year) VALUES (?)", graduation_years)

# Create updated students table
cur.execute("DROP TABLE IF EXISTS students")
cur.execute("""
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    email TEXT,
    gender TEXT CHECK(gender IN ('M', 'F', 'Other')),
    enrollment_date DATE,
    grade_level_id INTEGER,
    graduation_year_id INTEGER,
    FOREIGN KEY (grade_level_id) REFERENCES grade_levels(grade_level_id),
    FOREIGN KEY (graduation_year_id) REFERENCES graduation_years(graduation_year_id)
)
""")

# Fetch grade_level_ids and graduation_year_ids
cur.execute("SELECT grade_level_id FROM grade_levels")
grade_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT graduation_year_id FROM graduation_years")
grad_year_ids = [row[0] for row in cur.fetchall()]

# Populate students with randomized references
students_data = []
for _ in range(2500):
    first = fake.first_name()
    last = fake.last_name()
    dob = fake.date_of_birth(minimum_age=14, maximum_age=19)
    email = f"{first.lower()}.{last.lower()}@example.com"
    gender = random.choice(['M', 'F', 'Other'])
    enroll_date = fake.date_between(start_date='-4y', end_date='today')
    grade_id = random.choice(grade_ids)
    grad_id = random.choice(grad_year_ids)
    students_data.append((first, last, dob, email, gender, enroll_date, grade_id, grad_id))

cur.executemany("""
INSERT INTO students 
(first_name, last_name, date_of_birth, email, gender, enrollment_date, grade_level_id, graduation_year_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", students_data)

conn.commit()
conn.close()
"/mnt/data/student_mgmt.db created and populated successfully."
