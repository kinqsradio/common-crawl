import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def plot_sales_trends(database_name, username, password, host='localhost', port=5433):
    try:
        # Create the database URL
        database_url = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"

        # Create the SQLAlchemy engine
        engine = create_engine(database_url)

        # Query to get domain sales data
        query = "SELECT date, price FROM domain_sales WHERE price IS NOT NULL;"

        # Use pandas to read the SQL query into a DataFrame
        df = pd.read_sql_query(query, engine)

        # Convert the 'date' column to datetime, ensuring UTC conversion
        df['date'] = pd.to_datetime(df['date'], utc=True)

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['price'], marker='o', linestyle='-')
        plt.title('Domain Sales Prices Over Time')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.show()

    except Exception as error:
        print("Error connecting to the database:", error)

# Example usage
database_name = 'nineprimes'
username = 'anhdang'
password = '123456'

plot_sales_trends(database_name, username, password)
