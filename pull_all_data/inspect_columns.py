import psycopg2

def print_column_names(table_name):
    conn = psycopg2.connect(
        dbname="commoncrawl_db",
        user="anhdang",
        password="",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    query = f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
    """
    cursor.execute(query)
    columns = cursor.fetchall()

    print(f"Columns in table '{table_name}':")
    for column in columns:
        print(column[0])

    cursor.close()
    conn.close()

if __name__ == "__main__":
    print_column_names('warc_records')
