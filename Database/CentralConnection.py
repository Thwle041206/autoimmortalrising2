'''Status: Doing
Result:
- We create a central connection for all the classes to interact with the database.
'''
from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

# Database connection URL
DATABASE_URL = "mysql+pymysql://username:password@host:port/database"

# Set up the SQLAlchemy engine, base, and session
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

