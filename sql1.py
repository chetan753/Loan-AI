import sqlite3


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Average score per course
cursor.execute(
    """
    SELECT
        students.name,
        courses.course_name,
        MAX(grades.score) AS max_score
    FROM students
    INNER JOIN grades  ON students.id = grades.student_id
    INNER JOIN courses ON grades.student_course = courses.id  
    GROUP BY courses.course_name 
       
    """
)

print(f"{'Name':<15} | {'course':<10} | {'score':<6}")
print("-" * 30)
for row in cursor.fetchall():
    print(f"{row[0]:<15} | {row[1]:<10} | {row[2]:<6.2f}")

conn.close()