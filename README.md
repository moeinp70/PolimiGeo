# ES-project
# Flood Risk Analysis Project

This project provides a dashboard for analyzing flood risk data in Italy. It allows users to view maps of flood risk, generate reports, and visualize data. There are two types of users: regular users and admin users. Admin users can update the database.

## Features

- View flood risk data on an interactive map
- Generate reports in CSV and Excel formats
- Visualize data using a pie chart
- User authentication with different roles (user and admin)

## Requirements

- Python 3.7+
- PostgreSQL
- The following Python packages (listed in `requirements.txt`):
  - Flask
  - psycopg2
  - pandas
  - geopandas
  - folium
  - branca
  - requests
  - werkzeug
  - IPython
  - plotly
  - xlsxwriter
  - matplotlib
  - fpdf

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/moeinp70/PolimiGeo.git
    cd PolimiGeo
    ```

2. **Create a virtual environment and install the required packages:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Setup PostgreSQL database:**

    - Create a new PostgreSQL database named `flood_se`.
    - Update the `get_db_connection` function in `functions.py` if your database credentials are different.

4. **Run the `fetch_db_final.py` script to populate the database:**

    ```bash
    python fetch_db_final.py
    ```

5. **Run the Flask application (`app.py`):**

    ```bash
    python app.py
    ```

6. **Run the Jupyter Notebook for the dashboard:**

    ```bash
    jupyter notebook dashboard.ipynb
    ```

## Usage

- Open `dashboard.ipynb` in Jupyter Notebook.
- The first screen will prompt you to log in or sign up.
- Once logged in, you can view the dashboard:
  - Select the administrative level (province, region, or municipality).
  - Select a specific area to view detailed data and generate reports.
- Admin users can click the "Update Database" button to refresh the database with the latest data.

## Notes

- Ensure PostgreSQL server is running before starting the application.
- Default admin credentials: `username: admin`, `password: admin`.

## License

This project is licensed under the MIT License.
