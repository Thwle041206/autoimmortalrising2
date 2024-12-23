'''Status:Error - Uncheck
I dont know this TaskLogs is for what?
'''
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, Enum, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Step 1: Define Base for SQLAlchemy
Base = declarative_base()


# Define the DiscordAccount model
class DiscordAccount(Base):
    __tablename__ = 'discord_accounts'

    # Define the table columns
    id = Column(Integer, primary_key=True)  # Primary key
    username = Column(String, nullable=False)  # Username of the Discord account

    # Establish relationship to TaskLog (one-to-many from DiscordAccount to TaskLog)
    task_logs = relationship("TaskLog", back_populates="account")


# Define the Airdrop model
class Airdrop(Base):
    __tablename__ = 'airdrops'

    # Define the table columns
    id = Column(Integer, primary_key=True)  # Primary key
    airdrop_name = Column(String, nullable=False)  # Name of the airdrop

    # Establish relationship to TaskLog (one-to-many from Airdrop to TaskLog)
    task_logs = relationship("TaskLog", back_populates="airdrop")


# Define the TaskLog model
class TaskLog(Base):
    __tablename__ = 'task_logs'

    # Define the table columns
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key with auto-increment
    account_id = Column(Integer, ForeignKey('discord_accounts.id'), nullable=False)  # Foreign key to DiscordAccount
    airdrop_id = Column(Integer, ForeignKey('airdrops.id'), nullable=False)  # Foreign key to Airdrop
    action = Column(Text, nullable=False)  # Action performed in the task
    status = Column(Enum('success', 'failed'), default='success', nullable=False)  # Task status (default is 'success')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())  # Timestamp of task creation

    # Relationships to DiscordAccount and Airdrop
    account = relationship('DiscordAccount', back_populates='task_logs')
    airdrop = relationship('Airdrop', back_populates='task_logs')

    # String representation for easy debugging
    def __repr__(self):
        return f"<TaskLog(id={self.id}, action={self.action}, status={self.status}, created_at={self.created_at})>"


# CRUD functions for TaskLog
def create_task_log(session, account_id, airdrop_id, action, status='success'):
    """
    Function to create a new task log in the database.
    Args:
        session (Session): SQLAlchemy session instance.
        account_id (int): The ID of the Discord account performing the action.
        airdrop_id (int): The ID of the related airdrop.
        action (str): The action performed.
        status (str): The status of the action (success by default).
    """
    new_task_log = TaskLog(account_id=account_id, airdrop_id=airdrop_id, action=action, status=status)
    session.add(new_task_log)
    session.commit()  # Commit the transaction to the database
    return new_task_log


def get_task_logs_by_airdrop_id(session, airdrop_id):
    """
    Function to retrieve task logs by airdrop ID.
    Args:
        session (Session): SQLAlchemy session instance.
        airdrop_id (int): The ID of the airdrop for which task logs are fetched.
    """
    return session.query(TaskLog).filter(TaskLog.airdrop_id == airdrop_id).all()


def get_task_log_by_id(session, log_id):
    """
    Function to retrieve a task log by its ID.
    Args:
        session (Session): SQLAlchemy session instance.
        log_id (int): The ID of the task log.
    """
    return session.query(TaskLog).filter(TaskLog.id == log_id).first()


# Database connection setup
class ConnectDatabase:
    """
    Class for managing database connections using pymysql (for MySQL).
    """

    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            # Try connecting to the database using pymysql
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
    """
    Function to test the database connection.
    """
    db_connection = ConnectDatabase(
        host="8.219.149.132",  # Use actual DB host
        user="airdrop",
        password="ncsYSAT5y3cjtfwn",  # Replace with your actual password
        database="airdrop",  # Use actual database
        port=3306  # Use actual port
    )

    connection = db_connection.connect()
    if connection:
        print("Connection successful!")

        # Execute a query to fetch all tables (just a sample test)
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        query_result = cursor.fetchall()  # Fetch all results
        print(query_result)  # Print result (list of table names)
        db_connection.disconnect(connection)


# Main execution (example usage)
if __name__ == '__main__':
    # Create SQLAlchemy engine for an in-memory SQLite database (or connect to your MySQL)
    engine = create_engine('sqlite:///:memory:', echo=True)  # SQLite example for testing
    Base.metadata.create_all(engine)  # Create all tables

    # Create SQLAlchemy session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a new task log as an example
    new_task_log = create_task_log(session, 1, 1, 'Completed task', 'success')
    print(f"New Task Log: {new_task_log}")

    # Query for task logs related to a particular airdrop ID
    task_logs = get_task_logs_by_airdrop_id(session, 1)
    print(f"Task Logs for Airdrop ID 1: {task_logs}")

    # Close session when done
    session.close()
