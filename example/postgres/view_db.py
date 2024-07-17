import psycopg2
from psycopg2 import sql
import pandas as pd
from tabulate import tabulate

def connect_and_query(database_name, username, password, host='localhost', port=5432):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=database_name,
            user=username,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()
        
        # Query to get all tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        table_names = [table[0] for table in tables]
        print(tabulate(pd.DataFrame(table_names, columns=["Table Name"]), headers="keys", tablefmt="psql"))
        
        # Query to get the first 5 rows of each table
        for table in table_names:
            print(f"\nData from table {table}:")
            cursor.execute(sql.SQL("SELECT * FROM {} LIMIT 5;").format(sql.Identifier(table)))
            rows = cursor.fetchall()
            if rows:
                # Fetch column names
                column_names = [desc[0] for desc in cursor.description]
                # Create a DataFrame for pretty printing
                df = pd.DataFrame(rows, columns=column_names)
                print(tabulate(df, headers="keys", tablefmt="psql"))
            else:
                print("No data found.")
        
        cursor.close()
        connection.close()
    except Exception as error:
        print("Error connecting to the database:", error)

# Example usage
database_name = 'nineprimes'
username = 'anhdang'
password = '123456'

connect_and_query(database_name, username, password)
