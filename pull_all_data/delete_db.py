import psycopg2
from psycopg2 import sql

def delete_database():
    try:
        # Connect to the default PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="anhdang",
            password="",
            host="localhost",
            port="5433"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Drop the commoncrawl_db database
        cursor.execute("DROP DATABASE IF EXISTS commoncrawl_db")

        print("Database commoncrawl_db deleted successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting database: {e}")

if __name__ == "__main__":
    delete_database()
