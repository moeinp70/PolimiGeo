from functions import get_db_connection
import requests
import pandas as pd



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


"""
# Connect to the PostgreSQL database
db_name = "flood_se"
user = "postgres"
password = "admin"
host = "localhost"
conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host)
"""

# URLs for the datasets
def insert_data():
    urls = {
    "province": "https://idrogeo.isprambiente.it/api/pir/province/export",
    "region": "https://idrogeo.isprambiente.it/api/pir/regioni/export",
    "municipality": "https://idrogeo.isprambiente.it/api/pir/comuni/export"
    }

    # Fetch and insert data for each dataset
    for table_name, api_url in urls.items():
        fetch_and_insert_data(api_url, table_name)


# Create users table and add admin user

insert_data()


print("Flood-related data fetched and inserted into PostgreSQL tables successfully.")

