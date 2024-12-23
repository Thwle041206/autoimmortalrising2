'''Status: Successful
Result:
- connect Database
- show table's name in Database

http://8.219.149.132:888/phpmyadmin_782c63cbcdcb6970/server_databases.php
name: airdrop
password: ncsYSAT5y3cjtfwn

(CRUD operations: Create, Read, Update, Delete).
'''

import pymysql

class ConnectDatabase:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def connect(self):
        """Establishes a connection to the database."""
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            print("Database connection established!")
            return connection
        except pymysql.MySQLError as e:
            print(f"Error connecting to the database: {e}")
            return None

    def disconnect(self, connection):
        """Closes the database connection."""
        if connection:
            connection.close()
            print("Database connection closed!")


class DatabaseQuery:
    def __init__(self, connection):
        self.connection = connection  # Make sure to pass the actual connection object

    def execute_query(self, query):
        """Executes a query on the database."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            return None


def test_database_connection():
    # Initialize the ConnectDatabase class
    db_connection = ConnectDatabase(
        host="8.219.149.132",
        user="airdrop",
        password="ncsYSAT5y3cjtfwn",
        database="airdrop",
        port=3306  # Ensure this port is correct
    )

    # Establish connection
    connection = db_connection.connect()
    if connection:
        print("Connection successful!")

        # Create DatabaseQuery instance with the connection object
        db_query = DatabaseQuery(connection)

        # Example query: Show all tables
        query_result = db_query.execute_query("SHOW TABLES;")
        if query_result:
            print("Tables in the database:")
            for table in query_result:
                print(table)

        # Disconnect from the database
        db_connection.disconnect(connection)


if __name__ == "__main__":
    test_database_connection()




