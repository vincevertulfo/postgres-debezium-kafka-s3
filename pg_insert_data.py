import psycopg2

# Replace with your PostgreSQL credentials and database name
db_host = 'localhost'
db_port = '5433'
db_user = 'admin'
db_password = 'root'
db_name = 'food'

while True:
    try:
        # Establish connection
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

        # Create a cursor object using the connection
        cur = conn.cursor()

        # Ask user for ingredient name and price
        ingredient_name = input("Enter ingredient name: ")
        ingredient_price = input("Enter ingredient price: ")

        # Insert user input into database
        insert_query = "INSERT INTO ingredients (ingredient_name, ingredient_price) VALUES (%s, %s);"
        cur.execute(insert_query, (ingredient_name, ingredient_price))
        conn.commit()

        print(f"Successfully inserted '{ingredient_name}' with price '{ingredient_price}' into the database")
        # break  # Exit the loop if insertion is successful

    except psycopg2.Error as e:
        conn.rollback()  # Rollback any changes made so far in case of error
        print(f"Error inserting data: {e}")
        print("Please try again.\n")

    finally:
        if conn:
            cur.close()
            conn.close()