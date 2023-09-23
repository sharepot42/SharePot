from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from . import params
from .Logger import logger

user = params.PG_USER
password = params.PG_PASSWORD
host = params.PG_HOSTNAME
database = params.PG_DATABASE

#TODO before creating the conection to the database, grant all privileges to the user
#using:
# -> GRANT ALL PRIVILEGES ON SCHEMA public TO your_username;
# -> GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL #, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
