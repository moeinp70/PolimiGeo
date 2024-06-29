from flask import Flask, jsonify, request,session, redirect, url_for, send_file, render_template_string,send_from_directory
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



@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/', methods=['GET'])
def home():

    project_info = """
    <center><h1>Flood Risk Analysis Project</h1>
    <p>This project provides an analysis of flood risk across various administrative levels in Italy, including provinces, regions, and municipalities. The data is sourced from the IdroGEO API PIR (Hazards and risk indicators).</p>

    """
    about_us_html = open('about-us.html').read()
    
    # Read the HTML content of the flood_map_province.html file
    with open('flood_map_province.html', 'r') as file:
        map_html = file.read()
    
    full_content = project_info + about_us_html + map_html
    return render_template_string(full_content)


if __name__ == '__main__':
    app.run(debug=True)
