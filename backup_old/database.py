import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Connection details - Update these with your actual Postgres credentials
# Best practice is to use environment variables, but we'll use variables for now.
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "1234"

def connect_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                cursor_factory=RealDictCursor
            )
            cursor = conn.cursor()
            print("Database connection was successful!")
            return conn, cursor
        except Exception as error:
            print("Connecting to database failed")
            print("Error: ", error)
            time.sleep(2)

# Initialize connection
conn, cursor = connect_db()
