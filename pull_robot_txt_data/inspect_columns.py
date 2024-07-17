import psycopg2

def inspect_columns():
    conn = psycopg2.connect(
        dbname="common_crawl_robot_txt",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM robots_txt LIMIT 0;")
    colnames = [desc[0] for desc in cursor.description]
    print(colnames)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    inspect_columns()
