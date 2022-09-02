from os import getcwd, environ
from sys import modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Defines database session and engine for connecting to the database with
SQLAlchemy.

If the system is being tested, we create a mock sqllite db file and set up
the connection with that, otherwise we connect to the production database 
URL defined in the environment variables file.
"""

if "pytest" in modules:
    db_url = f'sqlite:///{getcwd()}/tests/data/test.db'
else:
    db_url = environ.get("DB_URL", None)
    
if "sqlite" in db_url:
    engine = create_engine(
    db_url, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
