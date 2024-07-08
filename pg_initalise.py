import psycopg2
from faker import Faker
 
# Replace with your PostgreSQL credentials and database name
db_host = 'localhost'
db_port = '5433'
db_user = 'admin'
db_password = 'root'
db_name = 'streaming'
 
 
def create_table_postgres(cursor, schema_name, table_name, create_query):
 
    # Drop table if exists
    cursor.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name}")
    print(f"Table '{schema_name}.{table_name}' dropped successfully.")
   
    # Create a table
    cursor.execute(create_query)
    print(f"Table '{schema_name}.{table_name}' created successfully.")
 
    # Alter table use all columns of the table's primary key or a
    # unique constraint to uniquely identify rows for replication purposes
    cursor.execute(f'ALTER TABLE {table_name} REPLICA IDENTITY FULL') # Do this so that Debezium can work correctly for CDC purposes
    print(f"Successfully set '{schema_name}.{table_name}' REPLICA IDENTITY to FULL.")
 
 
def populate_table_postgres(cursor, schema_name, table_name, insert_query, num_items):
 
    fake = Faker()
 
   # Generate dummy data
    data = []
    for _ in range(num_items):
        if table_name == 'products':
            product_name = fake.word()
            price = fake.random_number(digits=4) / 100.0  # Generate a price (e.g., 10.99)
            description = fake.sentence()
            data.append((product_name, price, description))
        elif table_name == 'employees':
            first_name = fake.first_name()
            last_name = fake.last_name()
            department = fake.job()
            hire_date = fake.date_between(start_date='-5y', end_date='today')
            data.append((first_name, last_name, department, hire_date))
 
    try:
        # Execute the insert query
        cursor.executemany(insert_query, data)
        print(f"{num_items} rows inserted into {schema_name}.{table_name} successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data into {schema_name}.{table_name}: {e}")
 
def main():
   
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
 
        # Create a cursor object using the connection
        cursor = conn.cursor()
 
        TABLE_CONFIG = {
            'products': {
                'CREATE_TBL_QUERY' : '''
                        CREATE TABLE products (
                            product_id SERIAL PRIMARY KEY,
                            product_name VARCHAR(100) NOT NULL,
                            price DECIMAL(10, 2) NOT NULL,
                            description TEXT
                        )
                    ''',
                'INSERT_TBL_QUERY': '''
                    INSERT INTO public.products (product_name, price, description)
                    VALUES (%s, %s, %s)
                ''',
                'NUM_ITEMS' : 20
            },
            'employees' : {
                'CREATE_TBL_QUERY' : '''
                        CREATE TABLE employees (
                            employee_id SERIAL PRIMARY KEY,
                            first_name VARCHAR(50) NOT NULL,
                            last_name VARCHAR(50) NOT NULL,
                            department VARCHAR(100),
                            hire_date DATE
                        )
                    ''',
                'INSERT_TBL_QUERY' : '''
                    INSERT INTO public.employees (first_name, last_name, department, hire_date)
                    VALUES (%s, %s, %s, %s)
                ''',
                'NUM_ITEMS' : 20
            }
        }
 
 
        for table in TABLE_CONFIG:
            print(table)
 
            # Create table
            create_table_postgres(cursor, schema_name='public', table_name=table, create_query=TABLE_CONFIG[table]['CREATE_TBL_QUERY'])
 
            # Insert dummy data into the table
            populate_table_postgres(cursor, schema_name='public', table_name=table, insert_query=TABLE_CONFIG[table]['INSERT_TBL_QUERY'], num_items=TABLE_CONFIG[table]['NUM_ITEMS'])
 
        # Close communication with the PostgreSQL database
 
        conn.commit()
        cursor.close()
 
    except Exception as e:
        print("Error executing SQL statement:", e)
 
    finally:
        # Close the database connection if it's open
        if conn is not None:
            conn.close()
            print('Database connection closed.')
           
if __name__ == "__main__":
    main()