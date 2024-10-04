import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

#create connection dict

DATABASE = {
    "host" : DATABASE_HOST,
    "database" : DATABASE_NAME,
    "user" : DATABASE_USER,
    "password" : DATABASE_PASSWORD
}

@contextmanager
def get_db():
    conn = psycopg2.connect(**DATABASE)
    try:
        yield conn
    except:
        conn.close()

    