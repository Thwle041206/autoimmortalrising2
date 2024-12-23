'''Status:Currently Successful
'''
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Define Base for SQLAlchemy
Base = declarative_base()

# Step 2: Database Connection
DATABASE_URL = 'mysql+pymysql://airdrop:ncsYSAT5y3cjtfwn@8.219.149.132:3306/airdrop'
engine = create_engine(DATABASE_URL, echo=True)  # echo=True to log SQL queries

# Create session maker
Session = sessionmaker(bind=engine)

# Step 3: Class Definition
class CRUD_DiscordAccount(Base):
    __tablename__ = 'discord_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    browser_id = Column(String(255), nullable=False)
    login_email = Column(String(255), nullable=False, unique=True)
    login_password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    email_password = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(255), nullable=True)
    is_alive = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def __repr__(self):
        return (
            f"<CRUD_DiscordAccount(id={self.id}, email={self.email}, is_alive={self.is_alive}, "
            f"token={self.token}, created_at={self.created_at})>"
        )

# CRUD operations
def create_discord_account(session, browser_id, login_email, login_password, email, email_password, token, phone_number=None):
    try:
        new_account = CRUD_DiscordAccount(
            browser_id=browser_id,
            login_email=login_email,
            login_password=login_password,
            email=email,
            email_password=email_password,
            token=token,
            phone_number=phone_number,
        )
        session.add(new_account)
        session.commit()  # Ensure commit to persist changes
        return new_account
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error during commit: {e}")
        return None

def get_discord_account_by_email(session, email):
    return session.query(CRUD_DiscordAccount).filter(CRUD_DiscordAccount.email == email).first()

def get_all_discord_accounts(session):
    return session.query(CRUD_DiscordAccount).all()

def update_discord_account(session, account_id, new_email=None, new_status=None):
    try:
        account = session.query(CRUD_DiscordAccount).filter(CRUD_DiscordAccount.id == account_id).first()
        if account:
            if new_email:
                account.email = new_email
            if new_status is not None:
                account.is_alive = new_status
            session.commit()  # Ensure commit to save changes
            return account
        return None
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error during commit: {e}")
        return None

def delete_discord_account(session, account_id):
    try:
        account = session.query(CRUD_DiscordAccount).filter(CRUD_DiscordAccount.id == account_id).first()
        if account:
            session.delete(account)
            session.commit()  # Commit the delete
            return True
        return False
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error during commit: {e}")
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
    # Testing code
    session = Session()

    try:
            # Create a new Discord account
            new_account = create_discord_account(
                session,
                browser_id="000000000",
                login_email="mtrsu4499@gmail.com",
                login_password="securepassword",
                email="test-email@example.com",
                email_password="emailpassword",
                token="unique-token-12345",
                phone_number="1234567890",
            )
            print(f"New Account: {new_account}")


    except Exception as e:
            print(f"Error: {e}")

    finally:
            session.close()
