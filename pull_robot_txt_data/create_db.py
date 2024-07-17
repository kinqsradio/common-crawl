import psycopg2

def create_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS common_crawl_robot_txt")
    cursor.execute("CREATE DATABASE common_crawl_robot_txt")

    cursor.close()
    conn.close()

def create_table():
    conn = psycopg2.connect(
        dbname="common_crawl_robot_txt",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS robots_txt (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            content TEXT
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def list_tables():
    conn = psycopg2.connect(
        dbname="common_crawl_robot_txt",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)

    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    create_table()
    list_tables()
