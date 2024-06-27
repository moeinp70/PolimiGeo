from flask import Flask, jsonify, request
import psycopg2
import pandas as pd
from functions import get_db_connection
app = Flask(__name__)

# Function to fetch data from PostgreSQL
def fetch_data_from_db(table_name):
    conn,_ = get_db_connection()
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient='records')

@app.route('/data/<level>', methods=['GET'])
def get_data(level):
    if level not in ['province', 'region', 'municipality']:
        return jsonify({"error": "Invalid level"}), 400
    
    data = fetch_data_from_db(level)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
