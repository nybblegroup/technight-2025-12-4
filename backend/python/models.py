"""
SQLAlchemy models for the application
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index
from sqlalchemy.sql import func
from database import Base


class Example(Base):
    """
    Example entity representing a sample record
    """
    __tablename__ = "example"
    
    # Unique identifier for the example
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Name of the example (required, max 200 chars)
    name = Column(String(200), nullable=False)
    
    # Title of the example (required, max 200 chars)
    title = Column(String(200), nullable=False)
    
    # Date when the example was entered (auto-set on creation)
    entry_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Optional description field (max 1000 chars)
    description = Column(String(1000), nullable=True)
    
    # Indicates if the example is active (default: true)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Index on entry_date for better query performance
    __table_args__ = (
        Index('ix_example_entry_date', 'entry_date'),
    )
    

