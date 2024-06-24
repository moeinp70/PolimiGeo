import requests
import psycopg2
import json


# Database connection parameters
db_name = "flood_se"
user = "postgres"
password = "admin"
host = "localhost"

# Connect to the PostgreSQL database
conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host)
cur = conn.cursor()

# Fetch data from IdroGEO API for provinces
url = 'https://idrogeo.isprambiente.it/api/pir/province/export'
response = requests.get(url)
data = response.json()

# Extract column names from the first record in the data
columns = list(data[0].keys())

# Create the table dynamically
create_table_query = f"""
CREATE TABLE IF NOT EXISTS province (
    id SERIAL PRIMARY KEY,
    {', '.join([f"{col} TEXT" for col in columns])}
);
"""
cur.execute(create_table_query)

# Insert data into the province table dynamically
insert_query = f"""
    INSERT INTO province ({', '.join(columns)}) VALUES %s
"""

# Prepare data for insertion
values = []
for record in data:
    record_values = [str(record.get(col, None)) for col in columns]
    values.append(tuple(record_values))

# Use psycopg2's execute_values for efficient bulk insertion
from psycopg2.extras import execute_values
execute_values(cur, insert_query, values)

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()

print("Data fetched and inserted into province table successfully.")
