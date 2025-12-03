"""
Pydantic schemas (DTOs) for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ExampleResponse(BaseModel):
    """
    Response schema for Example entity
    """
    id: int
    name: str
    title: str
    entryDate: datetime = Field(..., alias="entry_date")
    description: Optional[str] = None
    isActive: bool = Field(..., alias="is_active")
    image: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "First Example",
                "title": "Introduction",
                "entryDate": "2025-12-02T12:00:00Z",
                "description": "This is the first example entry",
                "isActive": True
            }
        }


class CreateExampleDto(BaseModel):
    """
    DTO for creating a new Example
    """
    name: str = Field(..., min_length=1, max_length=200, description="Name of the example")
    title: str = Field(..., min_length=1, max_length=200, description="Title of the example")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description field")
    isActive: Optional[bool] = Field(True, description="Indicates if the example is active")
    image: Optional[str] = Field(None, max_length=200, description="Optional image URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Example",
                "title": "Example Title",
                "description": "Optional description",
                "isActive": True
            }
        }


class UpdateExampleDto(BaseModel):
    """
    DTO for updating an existing Example (all fields optional)
    """
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Name of the example")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Title of the example")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description field")
    isActive: Optional[bool] = Field(None, description="Indicates if the example is active")
    image: Optional[str] = Field(None, max_length=200, description="Optional image URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Name",
                "title": "Updated Title",
                "description": "Updated description",
                "isActive": False
            }
        }

