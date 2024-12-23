'''Status:Currently Successful
Result:
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
import pymysql

# Define the Base class using the updated import
Base = declarative_base()

# Define the EmailAccount model (Assumed structure based on your columns)
class EmailAccount(Base):
    __tablename__ = 'email_accounts'

    id = Column(Integer, primary_key=True)
    browser_id = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=False)
    email_password = Column(String(255), nullable=False)
    backup_email = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)

# CRUD operations class for EmailAccount
class CRUD_EmailAccount:
    def __init__(self, session):
        self.session = session

    def create(self, browser_id, email_address, email_password, backup_email=None, phone_number=None):
        """Create a new EmailAccount."""
        new_account = EmailAccount(
            browser_id=browser_id,
            email_address=email_address,
            email_password=email_password,
            backup_email=backup_email,
            phone_number=phone_number,
        )
        self.session.add(new_account)
        try:
            self.session.commit()
            print(f"Created EmailAccount: {new_account}")
            return new_account
        except Exception as e:
            self.session.rollback()
            print(f"Failed to create EmailAccount: {e}")
            raise

    def get_by_email_address(self, email_address):
        """Retrieve an EmailAccount by email address."""
        try:
            account = self.session.query(EmailAccount).filter(EmailAccount.email_address == email_address).first()
            print(f"Retrieved EmailAccount: {account}")
            return account
        except Exception as e:
            print(f"Failed to retrieve EmailAccount: {e}")
            raise

    def update(self, email_address, **kwargs):
        """Update an existing EmailAccount."""
        try:
            account = self.get_by_email_address(email_address)
            if not account:
                print(f"No EmailAccount found with email_address: {email_address}")
                return None

            # Update fields dynamically from kwargs
            for field, value in kwargs.items():
                if hasattr(account, field):
                    setattr(account, field, value)
                else:
                    print(f"Invalid field: {field}")

            self.session.commit()
            print(f"Updated EmailAccount: {account}")
            return account
        except Exception as e:
            self.session.rollback()
            print(f"Failed to update EmailAccount: {e}")
            raise

    def delete(self, email_address):
        """Delete an EmailAccount by email address."""
        try:
            account = self.get_by_email_address(email_address)
            if not account:
                print(f"No EmailAccount found with email_address: {email_address}")
                return False

            self.session.delete(account)
            self.session.commit()
            print(f"Deleted EmailAccount: {account}")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Failed to delete EmailAccount: {e}")
            raise
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
        """Connect to the MySQL database."""
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
        """Disconnect the MySQL database."""
        if connection:
            connection.close()

# Step 1: Define the SQLAlchemy engine
def create_engine_and_session():
    # Create engine that points to MySQL (adjust based on your configuration)
    engine = create_engine('mysql+pymysql://airdrop:ncsYSAT5y3cjtfwn@8.219.149.132:3306/airdrop')
    # Create a configured sessionmaker
    Session = sessionmaker(bind=engine)
    return Session

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
    # Test the database connection
    test_database_connection()

    # Get session for CRUD operations
    Session = create_engine_and_session()
    session = Session()

    # Test CRUD_EmailAccount class
    crud_email = CRUD_EmailAccount(session)

    try:
        # Create a new email account
        new_account = crud_email.create(
            browser_id='000000000',
            email_address='mtrsu4488@gmail.com',
            email_password='Aa2234545!!',
            backup_email='backup@example.com',
            phone_number='123456789'
        )
        print("Created account:", new_account)
    except Exception as e:
        print(f"Error during operation: {e}")

    finally:
        session.close()
