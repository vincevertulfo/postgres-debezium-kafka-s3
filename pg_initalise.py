import psycopg2

# Replace with your PostgreSQL credentials and database name
db_host = 'localhost'
db_port = '5433'
db_user = 'admin'
db_password = 'root'
db_name = 'food'

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

        # Drop table if exists
        cursor.execute("DROP TABLE IF EXISTS public.ingredients")
        print("Table 'ingredients' dropped successfully.")
        
        # Create a table
        create_table_query = '''
            CREATE TABLE ingredients (
                ingredient_id SERIAL PRIMARY KEY, 
                ingredient_name VARCHAR(30) NOT NULL,
                ingredient_price INT NOT NULL,
                UNIQUE (ingredient_name)
            )
        '''
        cursor.execute(create_table_query)
        print("Table 'ingredients' created successfully.")
        
        # Alter table
        cursor.execute('ALTER TABLE ingredients REPLICA IDENTITY FULL') # Do this so that Debezium can work correctly

        # Insert dummy data into the table
        insert_query = '''
        INSERT INTO ingredients (ingredient_name, ingredient_price)
        VALUES
            (%s, %s)
        '''
        user_data = [
            ('Beef', 5),
            ('Chicken', 4),
            ('Pork', 7)
        ]
        cursor.executemany(insert_query, user_data)
        conn.commit()
        print("Data inserted successfully.")

        # Close communication with the PostgreSQL database
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