'''Status:Currently Successful
Result:
Database Connection Established: The connection to the MySQL database was successful.
Tables Retrieved: The list of tables, including browsers, was fetched successfully from the database.
Browser Record Inserted: The insertion of a new browser record (new_browser_id_001) into the browsers table was successful and committed.
Browser Record Retrieved: The SELECT query successfully retrieved the newly inserted browser record with id=8.
ROLLBACK at the End: The final ROLLBACK indicates that despite the successful operations, any ongoing transactions have been undone. This may happen if there is a transaction management issue, such as:
A call to rollback() in the code that undoes any changes to the database (possibly after an error, or the script might include a fallback after committing data).
Or an explicit call to rollback() at the end of the session to avoid leaving a pending transaction open.
Next Steps to Resolve
Check Explicit Commit or Rollback Calls: You might want to adjust your code to either explicitly commit changes or check for accidental rollbacks. Ensure that commits are happening after database operations that should be finalized.
Transaction Management: Modify your session handling so that transactions are explicitly managed. If there's no need to rollback explicitly, then avoid that unless something has gone wrong during the database operation.
'''
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymysql import MySQLError
import pymysql
from sqlalchemy import Column, Integer, String

# Define the base class for ORM models
Base = declarative_base()
class Browser(Base):
    __tablename__ = 'browsers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    browser_id = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<Browser(id={self.id}, browser_id={self.browser_id}, created_at={self.created_at})>"

DATABASE_URL = 'mysql+pymysql://airdrop:ncsYSAT5y3cjtfwn@8.219.149.132:3306/airdrop'
engine = create_engine(DATABASE_URL, echo=True)

# Initialize session and Base metadata
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def create_browser(session, browser_id):
    new_browser = Browser(browser_id=browser_id)
    session.add(new_browser)
    try:
        session.commit()
        print("Browser created and committed.")
    except Exception as e:
        session.rollback()
        print(f"Error during commit, rollback: {e}")
    return new_browser

# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE
# WE ADD NEW FUNCTION FOR CRUD TABLE BROWSERS HERE

# THIS FOR TEST
# Define the SQLAlchemy Base
Base = declarative_base()

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
        except MySQLError as e:
            print(f"Error connecting to the database: {e}")
            return None

    def disconnect(self, connection):
        """Closes the database connection."""
        if connection:
            connection.close()
            print("Database connection closed!")

def test_database_connection():
    # Create an instance of ConnectDatabase for connection
    db_connection = ConnectDatabase(
        host="8.219.149.132",
        user="airdrop",
        password="ncsYSAT5y3cjtfwn",
        database="airdrop",
        port=3306
    )

    # Establish connection to execute non-SQLAlchemy commands
    connection = db_connection.connect()
    if connection:
        print("Connection successful!")

        # Execute raw queries if needed
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        print(cursor.fetchall())  # List all tables
        db_connection.disconnect(connection)

###########################################################################
    # SQLAlchemy session for database CRUD operations
    session = Session()
    # CRUD operations like create, get, update, delete (add your functionality)
    browser = create_browser(session, "new_browser_id_004") # THIS ID "new_browser_id_001" JUST FOR TEST
    print(browser)
    session.close()

if __name__ == "__main__":
    test_database_connection()
