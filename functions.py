import requests
import pandas as pd
import geopandas as gpd
import folium
from branca.colormap import linear
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from IPython.display import FileLink
import plotly.express as px

def get_db_connection():
    # Database connection parameters
    db_name = "flood_se"
    user = "postgres"
    password = "admin"
    host = "localhost"
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host)
    cur = conn.cursor()
    return conn,cur

# Function to fetch data from API and insert into PostgreSQL table
def fetch_and_insert_data(api_url,table_name):

    # Connect to the PostgreSQL database
    conn,cur = get_db_connection()
    # Load translation file and create a list of flood-related columns
    translation_df = pd.read_csv('Metadata_PIR_translation.csv')
    flood_related_columns = translation_df.loc[translation_df['VARIABILE_INDICATORE'].str.contains('idr|idp|arid|pop_idr|fam_idr|ed_idr|im_idr|bbcc_id|tot|pop_res', case=False, regex=True), 'VARIABILE_INDICATORE'].tolist()
    response = requests.get(api_url)
    data = response.json()
    
    # Extract column names from the first record in the data
    columns = [col for col in data[0].keys() if col in flood_related_columns or col in ['cod_reg', 'cod_prov', 'provincia', 'comune', 'regione']]
    
    # Create the table dynamically
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        {', '.join([f"{col} TEXT" for col in columns])}
    );
    """
    cur.execute(create_table_query)
    
    # Insert data into the table dynamically
    insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s
    """
    
    # Prepare data for insertion
    values = []
    for record in data:
        record_values = [str(record.get(col, None)) for col in columns]
        values.append(tuple(record_values))
    
    # Use psycopg2's execute_values for efficient bulk insertion
    from psycopg2.extras import execute_values

    execute_values(cur, insert_query, values)

    conn.commit()
    cur.close()
    conn.close()



def create_users_table():
    conn,cur = get_db_connection()
    #cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_admin_user():
    conn,cur = get_db_connection()
    #cur = conn.cursor()
    hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING;", ('admin', hashed_password, 'admin'))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting admin user: {e}")
    cur.close()
    conn.close()



def signup_user(username, password, role='user'):
    conn,cur = get_db_connection()
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        conn.commit()
        result = "User signed up successfully!"
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        result = "Username already exists!"
    cur.close()
    conn.close()
    return result

def login_user(username, password):
    conn,cur = get_db_connection()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and check_password_hash(user[2], password):
        return user[3]  # Return user role
    else:
        return None

def fetch_data(level):
    url = f"http://localhost:5000/data/{level}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def load_shapefile(level):
    shapefile_paths = {
        'province': 'ProvCM01012024_g/ProvCM01012024_g_WGS84.shp',
        'region': 'Reg01012024_g/Reg01012024_g_WGS84.shp',
        'municipality': 'Com01012024_g/Com01012024_g_WGS84.shp'
    }
    shapefile_path = shapefile_paths[level]
    gdf = gpd.read_file(shapefile_path)
    return gdf

def create_map(level, specific=None):
    df = fetch_data(level)
    gdf = load_shapefile(level)
    
    if level == 'province':
        merge_column = 'DEN_UTS'
        data_column = 'provincia'
    elif level == 'region':
        merge_column = 'DEN_REG'
        data_column = 'regione'
    elif level == 'municipality':
        merge_column = 'COMUNE'
        data_column = 'comune'
    
    # Aggregate data to ensure unique values in the key column
    aggregation_functions = {col: 'first' for col in df.columns if col != data_column}
    df_aggregated = df.groupby(data_column).agg(aggregation_functions).reset_index()
    
    # Merge the dataframes
    merged_gdf = gdf.merge(df_aggregated, left_on=merge_column, right_on=data_column, how='left')
    
    # Calculate risk percentages and handle None values
    merged_gdf['risk_percentage'] = pd.to_numeric(merged_gdf['aridp3_p'], errors='coerce').fillna(0)
    
    # Create color scale based on overall range of flood risk percentages
    overall_min = merged_gdf['risk_percentage'].min()
    overall_max = merged_gdf['risk_percentage'].max()
    colormap = linear.YlOrRd_09.scale(overall_min, overall_max)
    colormap.caption = 'Percentage of Area at High Flood Risk'
    
    # Create a Folium map centered on Italy
    
    m = folium.Map(tiles=None,location=[41.8719, 12.5674], zoom_start=6)

        # Add different tile layers
    # Add OpenStreetMap tile layer
    folium.TileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', name='OpenTopoMap', attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)').add_to(m)
    folium.TileLayer('openstreetmap',name='OpenStreetMap', control=True).add_to(m)

    if specific:
        # Filter for specific selection if provided
        merged_gdf = merged_gdf[merged_gdf[merge_column] == specific]

    # Add the GeoJson layer with color coding based on flood risk percentage
    def style_function(feature):
        return {
            'fillColor': colormap(feature['properties']['risk_percentage']),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.4,
        }

    folium.GeoJson(
        merged_gdf,
        name="Flood Data",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=[
                data_column, 'aridp3_p', 'pop_idr_p3', 'fam_idr_p3',
                'ed_idr_p3', 'im_idr_p3', 'bbcc_id_p3'
            ],
            aliases=[
                'Province:' if level == 'province' else 'Region:' if level == 'region' else 'Municipality:', 
                'Percentage of Area at High Flood Risk (%):', 'Population at High Flood Risk:', 
                'Families at High Flood Risk:', 'Buildings at High Flood Risk:', 
                'Business Units at High Flood Risk:', 'Cultural Heritage at High Flood Risk:'
            ],
            localize=True
        )
    ).add_to(m)
    
    # Add colormap to the map
    colormap.add_to(m)
    
    # Add layer control to the map
    folium.LayerControl().add_to(m)
    
    # Save and display the map
    map_filename = f"flood_map_{level}.html"
    m.save(map_filename)
    return m, map_filename

def generate_report(level, specific, file_format='csv'):

    df = fetch_data(level)
    data_column = 'provincia' if level == 'province' else 'regione' if level == 'region' else 'comune'
    #filtered_df = df[df[data_column] == specific].iloc[[0,0]].copy()

    aggregation_functions = {col: 'first' for col in df.columns if col != data_column}
    df_aggregated = df.groupby(data_column).agg(aggregation_functions).reset_index()
    
    filtered_df = df_aggregated[df_aggregated[data_column] == specific].copy()
    
    translation_df = pd.read_csv('Metadata_PIR_translation.csv')
    header_translation = dict(zip(translation_df['VARIABILE_INDICATORE'], translation_df['DEFINITIONS']))
    filtered_df.rename(columns=header_translation, inplace=True)

    total_population = filtered_df['Resident population - 2011 Census (no. of inhabitants)'].values[0]
    high_risk_population = filtered_df['Population at  high flood risk (no. of inhabitants)'].values[0]
    medium_risk_population = filtered_df['Population at  medium flood risk (no. of inhabitants)'].values[0]
    low_risk_population = filtered_df['Population at  low flood risk (no. of inhabitants)'].values[0]
    
    total_buildings = filtered_df['Buildings - 2011 Census (n.)'].values[0]
    high_risk_buildings = filtered_df['Buildings at  high flood risk (n.)'].values[0]
    medium_risk_buildings = filtered_df['Buildings at  medium flood risk (n.)'].values[0]
    low_risk_buildings = filtered_df['Buildings at  low flood risk (n.)'].values[0]



    filtered_df = filtered_df.transpose().reset_index()
    filename = f"flood_risk_report_{specific}.{file_format}"
    
    '''
    df = fetch_data(level)
    # Correct the column name used for filtering
    data_column = 'provincia' if level == 'province' else 'regione' if level == 'region' else 'comune'
    
    # Aggregate data to ensure unique values in the key column
    aggregation_functions = {col: 'first' for col in df.columns if col != data_column}
    df_aggregated = df.groupby(data_column).agg(aggregation_functions).reset_index()
    
    filtered_df = df_aggregated[df_aggregated[data_column] == specific]
    
    # Translate column headers
    translation_df = pd.read_csv('Metadata_PIR_translation.csv')
    header_translation = dict(zip(translation_df['VARIABILE_INDICATORE'], translation_df['DEFINITIONS']))
    filtered_df.rename(columns=header_translation, inplace=True)
    
    # Convert to vertical format
    filtered_df = filtered_df.transpose().reset_index()
    filtered_df.columns = ['Indicator', 'Value']
    
    filename = f"flood_risk_report_{specific}.{file_format}"
    '''

    print(f"The total population in {specific} is {total_population}. \n\n"
                    f"Out of this, {high_risk_population} people are at high flood risk, {medium_risk_population} people are at medium flood risk, "
                    f"and {low_risk_population} people are at low flood risk.\n\n"
                    f"In terms of buildings, there are a total of {total_buildings} buildings in {specific}.\n\n "
                    f"Out of these, {high_risk_buildings} buildings are at high flood risk, {medium_risk_buildings} buildings are at medium flood risk, "
                    f"and {low_risk_buildings} buildings are at low flood risk.")
    
   


    if file_format == 'csv':
        filtered_df.to_csv(filename, index=False)
    elif file_format == 'xlsx':
        filtered_df.to_excel(filename, index=False)
    
    return filename




# Function to create and display the Plotly chart
def create_population_buildings_risk_plot(level, specific):
    df = fetch_data(level)
    data_column = 'provincia' if level == 'province' else 'regione' if level == 'region' else 'comune'
    
    specific_data = df[df[data_column] == specific].iloc[0]
    
    # Debugging statements
    #print(f"Data for {specific}:")
    #print(specific_data)
    
    #risk_levels = ['High', 'Medium', 'Low', 'No Risk']
    risk_levels = ['No Risk',  'Low', 'Medium', 'High']

    # Ensure values are numeric and handle any potential errors
    try:
        population = [
            pd.to_numeric(int(specific_data['pop_res011']) - int(specific_data['pop_idr_p1']) + int(specific_data['pop_idr_p2']) + int(specific_data['pop_idr_p3']) , errors='coerce'),
            pd.to_numeric(specific_data['pop_idr_p1'], errors='coerce'),
            pd.to_numeric(specific_data['pop_idr_p2'], errors='coerce'),
            pd.to_numeric(specific_data['pop_idr_p3'], errors='coerce')
            
        ]
    except KeyError as e:
        print(f"KeyError: {e}")
        population = [0, 0, 0, 0]
    '''
    try:
        buildings = [
            pd.to_numeric(specific_data['ed_idr_p3'], errors='coerce'),
            pd.to_numeric(specific_data['ed_idr_p2'], errors='coerce'),
            pd.to_numeric(specific_data['ed_idr_p1'], errors='coerce')
        ]
    except KeyError as e:
        print(f"KeyError: {e}")
        buildings = [0, 0, 0]
        
    total_population = pd.to_numeric(specific_data['pop_res011'], errors='coerce')
    total_buildings = pd.to_numeric(specific_data['ed_tot'], errors='coerce')
    '''

    #risk_colors = ['blue', 'lightblue', 'orange', 'red']
    #color_discrete_map = dict(zip(risk_levels, risk_colors))
    
    # Pie chart for population distribution at different risk levels
    fig_pie = px.pie(
        values=population,
        names=risk_levels,
        title=f'Population Distribution at Different Flood Risk Levels in the {level} of {specific}',
        color_discrete_sequence=px.colors.sequential.RdBu_r
    )
    
    fig_pie.show()
