from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv

from Infrastructure.Exceptions.DatabaseException import PostgreSqlConnectionException

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, isolation_level="SERIALIZABLE", pool_size=10, max_overflow=5, pool_timeout=30, pool_recycle=1800)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    """
    Dependency that provides a database session.
    This function is used to create a new database session for each request.
    It yields a session object that can be used in the application.
    If an exception occurs, it logs the error and raises a custom exception.
    Finally, it ensures that the session is closed after use.

    Returns:
        Session: A SQLAlchemy session object for database operations.

    Raises:
        PostgreSqlConnectionException: If there is an error connecting to the PostgreSQL database.
    """
    db = SessionLocal()
    try:
        yield db
        
    except Exception as e:
        logging.error(f"Error: {e}")
        raise PostgreSqlConnectionException()
    
    finally:
        db.close()