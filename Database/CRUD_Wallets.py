'''Status:Currently Successful
'''
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Define the Wallet class with proper columns and data types
class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    browser_id = Column(String(50), nullable=False)  # Assuming it's a string type
    wallet_address = Column(String(255), nullable=False)  # Wallet address is required
    private_key = Column(String(255), nullable=False)  # Private key, should be encrypted in practice
    wallet_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<Wallet(id={self.id}, wallet_address={self.wallet_address}, wallet_name={self.wallet_name}, created_at={self.created_at})>"
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE EMAILACCOUNTS HERE
# Database connection test function
class ConnectDatabase:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return self.connection
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None

    def disconnect(self, connection):
        if connection:
            connection.close()

# Database connection test function
def test_database_connection():
    db_connection = ConnectDatabase(
        host="8.219.149.132",
        user="airdrop",
        password="ncsYSAT5y3cjtfwn",
        database="airdrop",
        port=3306
    )

    connection = db_connection.connect()
    if connection:
        print("Connection successful!")

        # Execute the query and fetch results
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        query_result = cursor.fetchall()  # Fetch all results
        print(query_result)  # Show all tables
        db_connection.disconnect(connection)

# Example usage
if __name__ == '__main__':
    # Create SQLAlchemy engine and session
    DATABASE_URL = 'mysql+pymysql://airdrop:ncsYSAT5y3cjtfwn@8.219.149.132:3306/airdrop'
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True to log SQL queries
    Session = sessionmaker(bind=engine)

    session = Session()  # Create session

    try:
        # Example of creating a new Wallet instance
        new_wallet = Wallet(
            browser_id="000000000",
            wallet_address="0x123abc456def7890...",
            private_key="encrypted_private_key",
            wallet_name="MainWallet"
        )
        session.add(new_wallet)
        session.commit()  # Save the wallet to the database
        print(f"New Wallet: {new_wallet}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        session.close()  # Close the session
