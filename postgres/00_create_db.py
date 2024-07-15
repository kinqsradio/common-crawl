import psycopg2

def create_database(database_name, username, password, host='localhost', port=5432):
    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(
            dbname='postgres',  # Connect to the default 'postgres' database
            user=username,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Create the new database
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"Database {database_name} created successfully.")
        
        cursor.close()
        connection.close()
    except Exception as error:
        print("Error creating the database:", error)

database_name = 'nineprimes'
username = 'anhdang'
password = '123456' 

create_database(database_name, username, password)
