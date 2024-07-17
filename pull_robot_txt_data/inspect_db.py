import psycopg2
import pandas as pd

# Database connection parameters
DB_PARAMS = {
    'dbname': 'common_crawl_robot_txt',
    'user': 'anhdang',
    'password': '',
    'host': 'localhost',
    'port': '5433'
}

def inspect_db():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, content FROM robots_txt LIMIT 10;")
    rows = cursor.fetchall()
    
    # Convert to DataFrame for better readability
    df = pd.DataFrame(rows, columns=['ID', 'URL', 'Content'])
    print(df)
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    inspect_db()
