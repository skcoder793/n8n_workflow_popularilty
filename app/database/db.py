from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the 'data' directory exists so SQLite doesn't fail on creation
if not os.path.exists('./data'):
    os.makedirs('./data')

# Updated to use data_base.db for better project identification
SQLALCHEMY_DATABASE_URL = "sqlite:///./data_base.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Required for SQLite with FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to provide a database session for each request.
    Ensures the connection is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()