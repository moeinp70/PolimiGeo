# SoftwareEngineering-project
<p>This project provides an analysis of flood risk across various administrative levels in Italy, including provinces, regions, and municipalities. The data is sourced from the IdroGEO API PIR (Hazards and risk indicators), and the shapefiles are acquired from ISTAT</p>

## Meet Our Team

<p align="center">
    <strong>Four Geoinformatics Engineering students at Politecnico di Milano</strong>
</p>

<table align="center" style="width:100%" >
  <tr>
    <td style="text-align:center; width:50%">
      <img src="images/moein.jpg" alt="Moein Zadeh" style="width: 150px; height: 150px; border-radius: 50%;" />
      <h3>Moein Zadeh</h3>
        <p>
            Born in Iran, Qom.<br>
            AI and Deep Learning enthusiast.<br>
            Adventure and Gardening
        </p>
      <p>
          <a href="mailto:seyed.peyghambar@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
          <a href="https://github.com/moeinp70" target="_blank"><i class="fab fa-github"></i> GitHub</a> |
          <a href="https://www.linkedin.com/in/moein-peyghambarzadeh/" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
      </p>
    </td>
    <td style="text-align:center; width:50%">
      <img src="images/saeid.jpg" alt="Saeed Mehdizadeh" style="width: 150px; height: 150px; border-radius: 50%;" />
      <h3>Saeed Mehdizadeh</h3>
      <p>										
        Born in Bijar , Iran <br>
        Remote sesning expert ... .<br>
        Main Hubby: Videography  </p>
      <p>
          <a href="mailto:saeed.mehdizadeh@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
          <a href="https://github.com/saeedmehdizadeh" target="_blank"><i class="fab fa-github"></i> GitHub</a> |
          <a href="https://www.linkedin.com/in/saeed-mehdizadeh-a7099320b/" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
      </p>
    </td>
  </tr>
  <tr>
    <td style="text-align:center; width:50%">
      <img src="images/vanessa.jpg" alt="Vanessa" style="width: 150px; height: 150px; border-radius: 50%;" />
      <h3>Vanessa Goletti</h3>
      <p>										Born in Italy, Viterbo <br>
										Bcs in Management engineering.<br>
										Gym and climbing</p>
      <p>
          <a href="mailto:Vanessa.goletti@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
          <a href="https://github.com/Vanessabd" target="_blank"><i class="fab fa-github"></i> GitHub</a> |
          <a href="https://www.linkedin.com/in/vanessa-goletti-4b252b240/" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
      </p>
    </td>
    <td style="text-align:center; width:50%">
      <img src="images/hadi.jpg" alt="Hadi Kheiri" style="width: 150px; height: 150px; border-radius: 50%;" />
      <h3>Hadi Kheiri</h3>
      <p>										Born in Tabriz , Iran <br>
										Bcs in Geoinformatics eng.<br>
										Gym and Traveling  </p>
      <p>
          <a href="mailto:hadi.kheiri@mail.polimi.it"><i class="fas fa-envelope"></i> Mail</a> |
          <a href="https://github.com/Hadikheiri" target="_blank"><i class="fab fa-github"></i> GitHub</a> |
          <a href="https://www.linkedin.com/in/hadi-kheiri" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
      </p>
    </td>
  </tr>
</table>

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
