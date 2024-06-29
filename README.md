# ES-project


## Meet Our Team

<p align="center">
    <strong>Four Geoinformatics Engineering students at Politecnico di Milano</strong>
</p>

<div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;">
    <div style="flex: 0 0 23%; box-sizing: border-box; padding: 1em; margin-bottom: 2em;">
        <img src="images/moein.jpg" alt="Moein Zadeh" style="width: 100%; border-radius: 50%;" />
        <h3>Moein Zadeh</h3>
        <p>
            Born in Iran, Qom.<br>
            BSc in Computer Engineering at Shahab-Danesh University In Iran.<br>
            AI and Deep Learning enthusiast. Main hobby: Gardening
        </p>
        <p>
            <a href="mailto:seyed.peyghambar@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
            <a href="https://github.com/moeinp70"><i class="fab fa-github"></i> GitHub</a> |
            <a href="https://www.linkedin.com/in/moein-peyghambarzadeh/"><i class="fab fa-linkedin"></i> LinkedIn</a>
        </p>
    </div>

    <div style="flex: 0 0 23%; box-sizing: border-box; padding: 1em; margin-bottom: 2em;">
        <img src="images/saeed.jpg" alt="Saeed Mehdizadeh" style="width: 100%; border-radius: 50%;" />
        <h3>Saeed Mehdizadeh</h3>
        <p>[Include Saeed's bio here]</p>
        <p>
            <a href="mailto:saeed.mehdizadeh@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
            <a href="https://github.com/saeedmehdizadeh"><i class="fab fa-github"></i> GitHub</a> |
            <a href="https://www.linkedin.com/in/saeed-mehdizadeh/"><i class="fab fa-linkedin"></i> LinkedIn</a>
        </p>
    </div>

    <div style="flex: 0 0 23%; box-sizing: border-box; padding: 1em; margin-bottom: 2em;">
        <img src="images/vanessa.jpg" alt="Vanessa" style="width: 100%; border-radius: 50%;" />
        <h3>Vanessa</h3>
        <p>[Include Vanessa's bio here]</p>
        <p>
            <a href="mailto:vanessa@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
            <a href="https://github.com/vanessa"><i class="fab fa-github"></i> GitHub</a> |
            <a href="https://www.linkedin.com/in/vanessa/"><i class="fab fa-linkedin"></i> LinkedIn</a>
        </p>
    </div>

    <div style="flex: 0 0 23%; box-sizing: border-box; padding: 1em; margin-bottom: 2em;">
        <img src="images/hadi.jpg" alt="Hadi Kheiri" style="width: 100%; border-radius: 50%;" />
        <h3>Hadi Kheiri</h3>
        <p>[Include Hadi's bio here]</p>
        <p>
            <a href="mailto:hadi.kheiri@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
            <a href="https://github.com/hadi.kheiri"><i class="fab fa-github"></i> GitHub</a> |
            <a href="https://www.linkedin.com/in/hadi-kheiri/"><i class="fab fa-linkedin"></i> LinkedIn</a>
        </p>
    </div>
</div>


# Flood Risk Analysis Project

This project provides a dashboard for analyzing flood risk data in Italy. It allows users to view maps of flood risk, generate reports, and visualize data. There are two types of users: regular users and admin users. Admin users can update the database.

## Features

- View flood risk data on an interactive map
- Generate reports in CSV and Excel formats
- Visualize data using charts
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
  - jupyter
  - ipykernel

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

3. **Install Jupyter Notebook and IPython Kernel:**

    ```bash
    pip install jupyter ipykernel
    python -m ipykernel install --user --name=venv
    ```

4. **Setup PostgreSQL database:**

    - Create a new PostgreSQL database named `flood_se`.
    - Update the `get_db_connection` function in `functions.py` if your database credentials are different.

5. **Run the `fetch_db_final.py` script to populate the database:**

    ```bash
    python fetch_db_final.py
    ```

6. **Run the Flask application (`app.py`):**

    ```bash
    python app.py
    ```

7. **Run the Jupyter Notebook for the dashboard:**

    ```bash
    jupyter notebook
    ```

8. **Select the Virtual Environment Kernel:**

    - Open `dashboard.ipynb` in Jupyter Notebook.
    - Click on `Kernel` > `Change kernel` > `venv`.

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
