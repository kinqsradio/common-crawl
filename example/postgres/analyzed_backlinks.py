import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def analyze_backlinks(database_name, username, password, host='localhost', port=5432):
    try:
        # Create the database URL
        database_url = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"

        # Create the SQLAlchemy engine
        engine = create_engine(database_url)

        # Query to get backlink data
        query = "SELECT root_domain, page, title, spam_score FROM moz_link_data;"

        # Use pandas to read the SQL query into a DataFrame
        df = pd.read_sql_query(query, engine)

        # Analyze spam scores
        spam_score_counts = df['spam_score'].value_counts().sort_index()

        # Plot spam score distribution
        plt.figure(figsize=(10, 6))
        spam_score_counts.plot(kind='bar')
        plt.title('Distribution of Spam Scores in Backlinks')
        plt.xlabel('Spam Score')
        plt.ylabel('Count')
        plt.grid(True)
        plt.show()

        # Identify high-quality backlinks
        high_quality_backlinks = df[df['spam_score'] <= 3]
        print("High-Quality Backlinks (Spam Score <= 3):")
        print(high_quality_backlinks[['root_domain', 'page', 'title']])

    except Exception as error:
        print("Error connecting to the database:", error)

# Example usage
database_name = 'nineprimes'
username = 'anhdang'
password = '123456'

analyze_backlinks(database_name, username, password)
