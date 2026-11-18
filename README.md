<h1 align="center">SQL Injection and Student Grade Privacy</h1>
<p align="center">
  <img alt="Subject: Cyber Security" src="https://img.shields.io/badge/Subject-Cyber%20Security-56349B?style=flat-square">
  <img alt="Demo: Student Portal" src="https://img.shields.io/badge/Demo-Student%20Portal-087F76?style=flat-square">
  <img alt="Database: SQLite" src="https://img.shields.io/badge/Database-SQLite-205A9E?style=flat-square">
</p>

| Submitted by | Roll No. | Subject | Submitted to |
| :--- | :---: | :--- | :--- |
| **Salman Sohail** | **2652** | Cyber Security | Shah Muhammad |

Salman opens her student portal to check her grade. She should see one result: **B+**. If Bilal’s and Waheed’s grades appear alongside hers, their privacy has been compromised even though no grade has changed. This assignment uses that scenario to explain SQL injection, its effect on confidentiality, and how a parameterized query retrieves the correct record.

## Run the classroom demo

1. Download and extract the repository files.
2. Open [index.html](./index.html) from the extracted folder in a browser. The demo runs offline.
3. Select the three views in order. Watch the signed-in name as the rows change.

| Portal view | Visible grades | What to point out |
| :--- | :--- | :--- |
| 🔵 **Normal view** | Salman · B+ | One signed-in student sees her own record. |
| 🟠 **Simulated exposure** | Salman · B+, Bilal · A, Waheed · B | Salman is still signed in. Two classmates’ grades are now visible to her. |
| 🟢 **Protected view** | Salman · B+ | The displayed query has a placeholder for the signed-in student’s ID. |

> [!NOTE]
> The browser displays three prepared views with fictional records. The separate Python exercise below executes the protected query in SQLite.

## How the protection works

SQL injection can occur when an application mixes user input into the text of a SQL command. The database may then interpret part of that input as an instruction. In the grade portal scenario, changing which rows a query returns could expose another student’s grade.

The lookup in [verify.py](./verify.py) keeps the SQL statement fixed and supplies the ID separately:

```python
def my_grades(session_student_id):
    return db.execute(
        "SELECT grade FROM grades WHERE student_id = ?", (session_student_id,)
    ).fetchall()
```

**What keeps the query fixed?** SQLite binds the supplied value to the `?` placeholder. The value cannot change the structure of the statement.

**What determines whose grade appears?** The `WHERE` clause selects the row for the supplied student ID. A real portal should obtain that ID from the authenticated session. This exercise uses fixed IDs to represent sessions.

## Verify the results

With Python 3 installed, open a terminal in the extracted folder. Run `py verify.py` on Windows or `python3 verify.py` on macOS or Linux. The script creates an in-memory database and checks all four lookups using Python’s standard library.

```text
PASS | student 101 | grades [('B+',)]
PASS | student 102 | grades [('A',)]
PASS | student 103 | grades [('B',)]
PASS | student 999 | grades []
```

The first three checks each return one student’s grade. The fourth checks an unknown student ID. Its empty result confirms that an unmatched ID receives no grade.

## Further reading

[OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
