import psycopg2

def save_to_db(url, content_type, content):
    # Sanitize content by removing NULL characters
    sanitized_content = content.replace('\x00', '')

    conn = psycopg2.connect(
        dbname="commoncrawl_db",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO warc_records (url, content_type, content) VALUES (%s, %s, %s)
    """, (url, content_type, sanitized_content))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    url = "example_url"
    content_type = "example_content_type"
    content = "example_content"
    save_to_db(url, content_type, content)
