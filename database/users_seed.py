
# Creates login accounts for two doctors and two patients from existing data.
# Passwords are hashed with bcrypt before storing.
# Run once from the project root:
# py database/users_seed.py

import sys
from pathlib import Path

import mysql.connector
import bcrypt

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import get_db_connection

# Connect using the central configuration in backend/config.py
conn = get_db_connection()
cur = conn.cursor(dictionary=True)

print("Connected to caresync.")


# Helper: hash a plain password
def make_hash(plain_password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode(), salt).decode()


# Pick two real doctors from the database
cur.execute("SELECT doctor_id, full_name FROM doctor LIMIT 2")
doctors = cur.fetchall()

if len(doctors) < 2:
    print("ERROR: Need at least 2 doctors in the database.")
    cur.close()
    conn.close()
    raise SystemExit(1)


# Pick two active patients from the database
cur.execute("""
    SELECT patient_id, full_name
    FROM patient
    WHERE is_deleted = 0
    LIMIT 2
""")
patients = cur.fetchall()

if len(patients) < 2:
    print("ERROR: Need at least 2 active patients in the database.")
    cur.close()
    conn.close()
    raise SystemExit(1)


# Build the list of accounts to insert
accounts = [
    {
        "email": "doctor1@caresync.local",
        "plain_password": "Doctor@1234",
        "role": "doctor",
        "linked_id": doctors[0]["doctor_id"],
        "name": doctors[0]["full_name"]
    },
    {
        "email": "doctor2@caresync.local",
        "plain_password": "Doctor@1234",
        "role": "doctor",
        "linked_id": doctors[1]["doctor_id"],
        "name": doctors[1]["full_name"]
    },
    {
        "email": "patient1@caresync.local",
        "plain_password": "Patient@1234",
        "role": "patient",
        "linked_id": patients[0]["patient_id"],
        "name": patients[0]["full_name"]
    },
    {
        "email": "patient2@caresync.local",
        "plain_password": "Patient@1234",
        "role": "patient",
        "linked_id": patients[1]["patient_id"],
        "name": patients[1]["full_name"]
    },
]


# Insert each account; skip if email already exists
for acc in accounts:
    hashed = make_hash(acc["plain_password"])

    try:
        cur.execute(
            """
            INSERT INTO users (email, password_hash, role, linked_id)
            VALUES (%s, %s, %s, %s)
            """,
            (acc["email"], hashed, acc["role"], acc["linked_id"])
        )

        conn.commit()
        print(
            f"Inserted: {acc['email']} "
            f"({acc['role']} - {acc['name']})"
        )

    except mysql.connector.IntegrityError:
        conn.rollback()
        print(f"Skipped (already exists): {acc['email']}")


cur.close()
conn.close()

print("\nSeed complete.")
print("\nDemo login accounts:")
print("Doctor:  doctor1@caresync.local")
print("Doctor:  doctor2@caresync.local")
print("Patient: patient1@caresync.local")
print("Patient: patient2@caresync.local")
