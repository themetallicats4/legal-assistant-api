import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_all_laws():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM laws;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_law_by_id(law_id):
    """
    Fetches a specific law by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM laws WHERE id = %s;", (law_id,))
    law = cursor.fetchone()
    cursor.close()
    conn.close()
    return law