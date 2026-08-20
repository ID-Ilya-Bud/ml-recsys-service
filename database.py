import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def postgres_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
        )
    except Exception as e:
        print("❌ Ошибка при подключении к базе данных.")
        raise e
    
    conn.autocommit = True

    return conn
