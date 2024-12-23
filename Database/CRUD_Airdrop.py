'''Status:Currently Successful
Result:
It seems like the insert and select operations are successfully carried out on the database,
but the ROLLBACK at the end indicates that there might have been a transaction that wasn't completed or committed properly. Here's a summary of what the log shows:
The connection to the database is successful.
An insert into the airdrops table was successfully committed, indicating that the airdrop information (name, description, status, browser_id) was inserted into the database.
A SELECT query to fetch the airdrops by ID was executed and returned a result (id, name, status, and created_at values), confirming that the data can be retrieved successfully.
The ROLLBACK at the end suggests that there might be an open transaction or something that caused a rollback to undo changes.
To ensure that the data is fully processed and committed, try checking the database after the script finishes running.
Also, ensure that there are no open transactions left, or adjust the script to manage transactions explicitly using commit() or rollback() where necessary.
'''
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

# Define the base class for ORM models
Base = declarative_base()

# Define your class inheriting from Base
class CRUD_Airdrop(Base):
    __tablename__ = 'airdrop'  # Table name in the database
    id = Column(Integer, primary_key=True)
    name = Column(String)

    __tablename__ = 'airdrops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum('pending', 'completed', 'failed'), default='pending')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    browser_id = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<CRUD_Airdrop(id={self.id}, name={self.name}, status={self.status}, created_at={self.created_at})>"

# Update DATABASE_URL to connect to MySQL instead of SQLite
DATABASE_URL = 'mysql+pymysql://airdrop:ncsYSAT5y3cjtfwn@8.219.149.132:3306/airdrop'

# Establish engine connection with MySQL
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables if they do not exist
Base.metadata.create_all(engine)

# Create session to interact with the database
Session = sessionmaker(bind=engine)

# CRUD operations (already defined as earlier)
def create_airdrop(session, name, description, browser_id):
    new_airdrop = CRUD_Airdrop(name=name, description=description, browser_id=browser_id)
    session.add(new_airdrop)
    session.commit()
    return new_airdrop

def get_all_airdrops(session):
    return session.query(CRUD_Airdrop).all()

def get_airdrop_by_id(session, airdrop_id):
    return session.query(CRUD_Airdrop).filter(CRUD_Airdrop.id == airdrop_id).first()

def update_airdrop_status(session, airdrop_id, status):
    airdrop = session.query(CRUD_Airdrop).filter(CRUD_Airdrop.id == airdrop_id).first()
    if airdrop:
        airdrop.status = status
        session.commit()
        return airdrop
    return None

def delete_airdrop(session, airdrop_id):
    airdrop = session.query(CRUD_Airdrop).filter(CRUD_Airdrop.id == airdrop_id).first()
    if airdrop:
        session.delete(airdrop)
        session.commit()

# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE AIRDROP HERE

# THIS FOR TEST
# Database connection class
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

# Step 1: Define Base for SQLAlchemy
Base = declarative_base()
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
    test_database_connection()
    session = Session()  # Create session
    new_airdrop = create_airdrop(session, 'Test Airdrop', 'Description of the test airdrop', '000000000')
    print(new_airdrop)
    session.close()
