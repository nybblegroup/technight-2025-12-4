"""
Database configuration and connection management using SQLAlchemy
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
# If DATABASE_URL is not set, create a None engine (for optional DB)
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using them
        pool_recycle=3600,   # Recycle connections after 1 hour
    )
else:
    engine = None

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session
    
    Yields:
        Session: SQLAlchemy database session
    """
    if SessionLocal is None:
        raise RuntimeError("Database not configured. Please set DATABASE_URL environment variable.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection() -> dict:
    """
    Check database connectivity
    
    Returns:
        dict: Connection status with details
    """
    if not engine:
        return {
            "connected": False,
            "error": "Database not configured. DATABASE_URL environment variable not set."
        }
    
    try:
        # Try to execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        
        return {
            "connected": True,
            "message": "Database connection successful"
        }
    except SQLAlchemyError as e:
        error_str = str(e)
        error_msg = error_str
        
        # Categorize common errors for better user experience
        if "invalid dsn" in error_str.lower() or "invalid connection option" in error_str.lower():
            error_msg = f"Invalid database connection string: {error_str}. Please check your DATABASE_URL format."
        elif "could not connect" in error_str.lower() or "connection refused" in error_str.lower():
            error_msg = f"Could not connect to database server: {error_str}. Is PostgreSQL running?"
        elif "authentication failed" in error_str.lower() or "password authentication failed" in error_str.lower():
            error_msg = f"Database authentication failed: {error_str}. Please check your credentials."
        elif "database" in error_str.lower() and "does not exist" in error_str.lower():
            error_msg = f"Database does not exist: {error_str}. Please create the database first."
        
        return {
            "connected": False,
            "error": error_msg
        }
    except Exception as e:
        error_str = str(e)
        # Check for connection-related errors
        if "connection" in error_str.lower() or "refused" in error_str.lower() or "timeout" in error_str.lower():
            return {
                "connected": False,
                "error": f"Connection error: {error_str}. Is PostgreSQL running and accessible?"
            }
        return {
            "connected": False,
            "error": f"Unexpected error: {error_str}"
        }

