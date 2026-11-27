import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

APP_NAME = "CareSync"
APP_VERSION = "1.1.0"
APP_DESCRIPTION = "Patient portal for hospital and clinic management"

DATABASE_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DB_PORT", "3306"))
DATABASE_NAME = os.getenv("DB_NAME")
DATABASE_USER = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")

if not all([DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, AUTH_SECRET_KEY]):
    raise ValueError("Missing required configuration. Check your root .env file.")

def get_db_connection():
    return mysql.connector.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )

ROLE_PATIENT = "patient"
ROLE_DOCTOR = "doctor"
ROLE_BILLING = "billing_staff"
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
