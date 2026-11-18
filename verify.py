"""Verify grade isolation with fictional session IDs and an in-memory database."""
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE grades (student_id INTEGER PRIMARY KEY, grade TEXT)")
db.executemany("INSERT INTO grades VALUES (?, ?)", [(101, "B+"), (102, "A"), (103, "B")])


def my_grades(session_student_id):
    return db.execute(
        "SELECT grade FROM grades WHERE student_id = ?", (session_student_id,)
    ).fetchall()


for student, expected in [(101, [("B+",)]), (102, [("A",)]), (103, [("B",)]), (999, [])]:
    actual = my_grades(student)
    if actual != expected:
        raise AssertionError((student, actual, expected))
    print(f"PASS | student {student} | grades {actual}")
db.close()
