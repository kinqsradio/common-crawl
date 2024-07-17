import psycopg2

def create_role(role_name, username, password, host='localhost', port=5433):
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
        
        # Create the new role
        cursor.execute(f"CREATE ROLE {role_name};")
        print(f"Role {role_name} created successfully.")
        
        cursor.close()
        connection.close()
    except Exception as error:
        print("Error creating the role:", error)

# Example usage
role_name = 'doadmin'
username = 'anhdang'
password = '123456'

create_role(role_name, username, password)
