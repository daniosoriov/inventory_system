import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection() -> psycopg2.extensions.connection:
    try:
        conn = psycopg2.connect(database=os.environ.get("DB_NAME"),
                                host=os.environ.get("DB_HOST"),
                                user=os.environ.get("DB_USER"),
                                password=os.environ.get("DB_PASS"),
                                port=os.environ.get("DB_PORT"))
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
        raise e


def get_db_cursor() -> psycopg2.extensions.cursor:
    conn = get_db_connection()
    print("Connected to PostgreSQL")
    return conn.cursor()
