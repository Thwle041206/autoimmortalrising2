'''Status:Currently Successful
'''
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Define Base for SQLAlchemy
Base = declarative_base()

# Step 2: Database Connection
DATABASE_URL = 'mysql+pymysql://airdrop:ncsYSAT5y3cjtfwn@8.219.149.132:3306/airdrop'
engine = create_engine(DATABASE_URL, echo=True)  # echo=True to log SQL queries

# Create session maker
Session = sessionmaker(bind=engine)

# Step 3: Define the TwitterAccount class
class TwitterAccount(Base):
    __tablename__ = 'twitter_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    browser_id = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    email_password = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    f2a_link = Column(String(255), nullable=True)
    is_alive = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<TwitterAccount(id={self.id}, username={self.username}, is_alive={self.is_alive})>"

# CRUD operations for TwitterAccount class
def create_twitter_account(session, browser_id, email, email_password, username, password, f2a_link=None):
    try:
        new_account = TwitterAccount(
            browser_id=browser_id, email=email, email_password=email_password,
            username=username, password=password, f2a_link=f2a_link)
        session.add(new_account)
        session.commit()  # Commit to persist changes
        return new_account
    except Exception as e:
        session.rollback()  # Rollback on error to ensure session consistency
        print(f"Error creating account: {e}")
        return None


def get_twitter_account_by_username(session, username):
    return session.query(TwitterAccount).filter(TwitterAccount.username == username).first()

def get_all_twitter_accounts(session):
    return session.query(TwitterAccount).all()

def update_twitter_account(session, account_id, new_email=None, new_status=None):
    account = session.query(TwitterAccount).filter(TwitterAccount.id == account_id).first()
    if account:
        if new_email:
            account.email = new_email
        if new_status is not None:
            account.is_alive = new_status
        try:
            session.commit()
            return account
        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error updating account: {e}")
            return None
    return None

def delete_twitter_account(session, account_id):
    account = session.query(TwitterAccount).filter(TwitterAccount.id == account_id).first()
    if account:
        try:
            session.delete(account)
            session.commit()
            return True
        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error deleting account: {e}")
            return False
    return False
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
    test_database_connection()
    session = Session()  # Create session


        # Create a new Twitter account
    new_account = create_twitter_account(
            session,
            browser_id="000000000",
            email="test-email@example.com",
            email_password="securepassword",
            username="testusername",
            password="userpassword",
            f2a_link="http://somef2a.com",
        )
    print(f"New Account: {new_account}")
    session.close()  # Close the session
