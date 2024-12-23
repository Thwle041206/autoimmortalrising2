from Database.ConnectDatabase import ConnectDatabase
from Database.ConnectDatabase import DatabaseQuery

'''Status: Successful: ConnectDatabase'''
def test_database_connection():
    # Initialize the DatabaseConnection class
    db_connection = ConnectDatabase(
        host="8.219.149.132",
        user="airdrop",
        password="ncsYSAT5y3cjtfwn",
        database="airdrop",
        port=3306
    )

    # Establish connection
    connection = db_connection.connect()
    if connection:
        print("Connection successful!")

        # Create DatabaseQuery instance using the actual connection object
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
