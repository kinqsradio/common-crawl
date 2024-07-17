import psycopg2

def inspect_db():
    conn = psycopg2.connect(
        dbname="commoncrawl_db",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM warc_records LIMIT 10;")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    inspect_db()
