import mysql.connector

try:
    # Replace these with your MySQL database credentials
    host = "localhost"
    user = "volkansql"
    password = "123"
    database = "discountsdb"

    # Establish a MySQL connection
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to MySQL database")

        # You can execute MySQL queries or operations here

        # Close the database connection
        connection.close()
        print("Connection closed")

except mysql.connector.Error as e:
    print(f"Error: {e}")
