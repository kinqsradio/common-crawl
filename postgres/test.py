import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def train_domain_valuation_model(database_name, username, password):
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname=database_name,
        user=username,
        password=password,
        host='localhost',
        port=5433
    )
    query = "SELECT * FROM domain_ai_classify WHERE attractive_score IS NOT NULL;"
    df = pd.read_sql_query(query, connection)
    connection.close()

    # Prepare the data
    X = df[['industry', 'location']]  # Add other relevant features
    y = df['attractive_score']
    X = pd.get_dummies(X)  # Convert categorical features to numeric

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')

    return model

# Example usage
database_name = 'nineprimes'
username = 'anhdang'
password = '123456'

model = train_domain_valuation_model(database_name, username, password)
