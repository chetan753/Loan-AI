import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS courses")
cursor.execute("DROP TABLE IF EXISTS grades")

# Create the table if it doesn't exist
cursor.execute("""
               CREATE TABLE students (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   age INTEGER,
                   city TEXT)""")

cursor.execute("""
               CREATE TABLE courses (
                   id INTEGER PRIMARY KEY,
                   course_name TEXT,
                   teacher TEXT,
                   duration_weeks INTEGER)""")

cursor.execute(f"""
               CREATE TABLE grades (
                   id INTEGER PRIMARY KEY,
                   student_id INTEGER,
                   student_course INTEGER,
                   score INTEGER)""")

cursor.executemany(
    "INSERT INTO students VALUES (?,?,?,?)",
    [
        (1, "Chetan",  21, "Mumbai"),
        (2, "Raj",     22, "Delhi"),
        (3, "Priya",   20, "Bangalore"),
        (4, "Aman",    23, "Mumbai"),
        (5, "Sneha",   21, "Delhi"),
    ]
)

# Insert courses
cursor.executemany(
    "INSERT INTO courses VALUES (?,?,?,?)",
    [
        (1, "Machine Learning", "Sharma",  12),
        (2, "Python",           "Verma",   8),
        (3, "SQL",              "Gupta",   6),
        (4, "Deep Learning",    "Sharma",  16),
    ]
)

# Insert grades (not every student takes every course)
cursor.executemany(
    "INSERT INTO grades VALUES (?,?,?,?)",
    [
        (1,  1, 1, 92),  # Chetan  → ML      → 92
        (2,  1, 2, 88),  # Chetan  → Python  → 88
        (3,  1, 3, 95),  # Chetan  → SQL     → 95
        (4,  2, 1, 74),  # Raj     → ML      → 74
        (5,  2, 2, 70),  # Raj     → Python  → 70
        (6,  3, 1, 97),  # Priya   → ML      → 97
        (7,  3, 4, 91),  # Priya   → Deep L  → 91
        (8,  4, 2, 58),  # Aman    → Python  → 58
        (9,  5, 1, 83),  # Sneha   → ML      → 83
        (10, 5, 3, 79),  # Sneha   → SQL     → 79
    ]
)

conn.commit()
conn.close()
print("data created")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

rows1 = cursor.execute(
    """
    SELECT 
        students.name,
        courses.course_name,
        COUNT(grades.score) AS count_score
    FROM grades
    INNER JOIN students ON grades.student_id = students.id
    INNER JOIN courses ON grades.student_course = courses.id
    GROUP BY students.name
    """
)

for i in rows1.fetchall():
    print(i)
    
conn.close()
    