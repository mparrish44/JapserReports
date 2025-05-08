import sqlite3

conn = sqlite3.connect("student_mgmt.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT g.grade_index, COUNT(s.student_id) as student_count
    FROM students s
    JOIN grade_levels g ON s.grade_level_id = g.grade_level_id
    GROUP BY g.grade_index
    ORDER BY g.grade_index
""")

results = cursor.fetchall()

print("📊 Students per Grade Level (by grade_index):")
for grade_index, count in results:
    print(f"Grade {grade_index:>2}: {count} students")

conn.close()
