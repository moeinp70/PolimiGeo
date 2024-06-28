from flask import Flask, jsonify, request,session, redirect, url_for, send_file, render_template_string
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

@app.route('/', methods=['GET'])
def home():
    project_info = """
    <h1>Flood Risk Analysis Project</h1>
    <p>This project provides an analysis of flood risk across various administrative levels in Italy, including provinces, regions, and municipalities. The data is sourced from the IdroGEO API PIR (Hazards and risk indicators).</p>
    <h2>Map of Flood Risk</h2>
    """
    
    # Read the HTML content of the flood_map_province.html file
    with open('flood_map_province.html', 'r') as file:
        map_html = file.read()
    
    full_content = project_info + map_html
    return render_template_string(full_content)

@app.route('/data/<level>', methods=['GET'])
def get_data(level):
    if level not in ['province', 'region', 'municipality']:
        return jsonify({"error": "Invalid level"}), 400
    
    data = fetch_data_from_db(level)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
