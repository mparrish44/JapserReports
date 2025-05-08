# Re-import necessary modules after state reset
import sqlite3
from faker import Faker
import random

# Re-initialize Faker and reconnect to the database
fake = Faker()
conn = sqlite3.connect("student_mgmt.db")
cursor = conn.cursor()

# Recreate the students table in case it doesn't exist (simplified)
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    email TEXT,
    gender TEXT,
    enrollment_date TEXT
)
""")

# Helper function for random gender
def random_gender():
    return random.choice(['M', 'F', 'Other'])

# Generate and insert 2500 fake students
students = []
for _ in range(2500):
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=25).strftime('%Y-%m-%d')
    email = fake.email()
    gender = random_gender()
    enrollment_date = fake.date_between(start_date='-4y', end_date='today').strftime('%Y-%m-%d')
    students.append((first_name, last_name, dob, email, gender, enrollment_date))

cursor.executemany("""
    INSERT INTO students (first_name, last_name, date_of_birth, email, gender, enrollment_date)
    VALUES (?, ?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

"2500 students successfully added to the student_mgmt.db database."
