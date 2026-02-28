import sqlite3

# إنشاء قاعدة البيانات
conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    risk REAL,
    diagnosis TEXT
)
""")

conn.commit()

# حفظ مريض
def save_patient(name, age, risk, diagnosis):
    cursor.execute(
        "INSERT INTO patients(name,age,risk,diagnosis) VALUES(?,?,?,?)",
        (name, age, risk, diagnosis)
    )
    conn.commit()

# جلب المرضى
def get_patients():
    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    return cursor.fetchall()
