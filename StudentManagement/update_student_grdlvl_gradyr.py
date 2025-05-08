import sqlite3
from datetime import datetime

# Load existing database
db_path = "student_mgmt.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Determine current year
current_year = datetime.now().year

# Update students table with grade_level_id and graduation_year_id
update_sql = """
UPDATE students
SET
    grade_level_id = CASE
        WHEN ? - CAST(strftime('%Y', enrollment_date) AS INTEGER) = 0 THEN 1
        WHEN ? - CAST(strftime('%Y', enrollment_date) AS INTEGER) = 1 THEN 2
        WHEN ? - CAST(strftime('%Y', enrollment_date) AS INTEGER) = 2 THEN 3
        ELSE 4
    END,
    graduation_year_id = (
        SELECT graduation_year_id
        FROM graduation_years
        WHERE year = CAST(strftime('%Y', enrollment_date) AS INTEGER) + 4
        LIMIT 1
    );
"""

cursor.execute(update_sql, (current_year, current_year, current_year))
conn.commit()
conn.close()

db_path  # Returning path to the updated database file.
