import psycopg2

def find_urls():
    conn = psycopg2.connect(
        dbname="commoncrawl_db",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM warc_records")
    urls = cursor.fetchall()

    print("URLs in the warc_records table:")
    for url in urls:
        print(url[0])

    cursor.close()
    conn.close()

if __name__ == "__main__":
    find_urls()
