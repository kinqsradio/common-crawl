import psycopg2

def delete_database():
    try:
        # Connect to the default PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="anhdang",
            password="",
            host="localhost",
            port="5433"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Drop the common_crawl_robot_txt database
        cursor.execute("DROP DATABASE IF EXISTS common_crawl_robot_txt")

        print("Database common_crawl_robot_txt deleted successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting database: {e}")

if __name__ == "__main__":
    delete_database()


# import psycopg2

# def delete_data():
#     try:
#         conn = psycopg2.connect(
#             dbname="common_crawl_robot_txt",
#             user="anhdang",
#             password="",
#             host="localhost",
#             port="5433"
#         )
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM robots_txt;")
        
#         print(f'Data in table robots_txt deleted successfully.')
        
#         conn.commit()
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         print(f"Error deleting data: {e}")

# if __name__ == '__main__':
#     delete_data()
