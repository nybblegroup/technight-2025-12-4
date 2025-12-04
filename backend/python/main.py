from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import os
import yaml
from dotenv import load_dotenv
import signal
import sys
import uvicorn
from database import check_database_connection, get_db
from models import Example
from schemas import ExampleResponse, CreateExampleDto, UpdateExampleDto

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Nybble Event Engagement Hub API",
    version="2.0.0",
    description="AI-powered event engagement platform with gamification, real-time chat, and analytics",
    docs_url="/api/swagger",
    openapi_url="/api/openapi.json",
)

PORT = int(os.getenv("PORT", 8080))

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routes import events, participants, questions, responses, messages, nybblers

# Include routers
app.include_router(events.router)
app.include_router(participants.router)
app.include_router(questions.router)
app.include_router(responses.router)
app.include_router(messages.router)
app.include_router(nybblers.router)

# Initialize badges on startup
from services.gamification_service import gamification_service
from database import SessionLocal

@app.on_event("startup")
async def startup_event():
    """Initialize database with badges and seed data"""
    try:
        db = SessionLocal()
        await gamification_service.seed_badges(db)
        db.close()
        print("✅ Badges seeded successfully")
    except Exception as e:
        print(f"⚠️  Error seeding badges: {e}")


# Response models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class DatabaseHealthResponse(BaseModel):
    """
    Database health check response model
    """
    connected: bool
    message: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime


@app.get("/api/health", tags=["Health"], operation_id="apiHealthGet", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint

    Returns the health status of the API

    Returns:
        HealthResponse: Health status with timestamp
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow()
    }


@app.get("/api/health/db", tags=["Health"], operation_id="apiHealthDbGet", response_model=DatabaseHealthResponse)
async def health_check_db():
    """
    Database connectivity check endpoint

    Verifies the connection status to the PostgreSQL database.
    Checks if the database is accessible and responding to queries.

    Returns:
        DatabaseHealthResponse: Database connection status with details
        
    Example responses:
        - Success: {"connected": true, "message": "Database connection successful", "timestamp": "..."}
        - Error: {"connected": false, "error": "Connection error details", "timestamp": "..."}
        - Not configured: {"connected": false, "error": "DATABASE_URL not set", "timestamp": "..."}
    """
    db_status = check_database_connection()
    
    return {
        "connected": db_status["connected"],
        "message": db_status.get("message"),
        "error": db_status.get("error"),
        "timestamp": datetime.utcnow()
    }


@app.get("/api/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    """
    Serve OpenAPI spec as YAML
    """
    openapi_schema = app.openapi()
    yaml_content = yaml.dump(openapi_schema, default_flow_style=False)
    return Response(content=yaml_content, media_type="text/yaml")


# ============================================================================
# Examples CRUD Endpoints
# ============================================================================

@app.get(
    "/api/examples",
    tags=["Examples"],
    operation_id="apiExamplesGet",
    response_model=List[ExampleResponse],
    summary="Get all examples",
    description="Retrieves all example records from the database, ordered by entry date descending"
)
async def get_all_examples(db: Session = Depends(get_db)):
    """
    Get all examples
    
    Returns a list of all examples ordered by entry date (newest first)
    """
    try:
        examples = db.query(Example).order_by(Example.entry_date.desc()).all()
        return examples
    except Exception as e:
        error_msg = str(e)
        # Check if it's a database connection error
        if "connection" in error_msg.lower() or "refused" in error_msg.lower() or "could not connect" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Database connection failed. Please ensure PostgreSQL is running and DATABASE_URL is correctly configured."
            )
        raise HTTPException(status_code=500, detail=f"Error fetching examples: {error_msg}")


@app.get(
    "/api/examples/search",
    tags=["Examples"],
    operation_id="apiExamplesSearchGet",
    response_model=List[ExampleResponse],
    summary="Search examples by name",
    description="Search examples by name (case-insensitive partial match)"
)
async def search_examples(
    name: str = Query(..., description="Name to search for"),
    db: Session = Depends(get_db)
):
    """
    Search examples by name
    
    Searches for examples where the name contains the provided string (case-insensitive)
    """
    try:
        examples = db.query(Example).filter(
            Example.name.ilike(f"%{name}%")
        ).order_by(Example.entry_date.desc()).all()
        return examples
    except Exception as e:
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower() or "could not connect" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Database connection failed. Please ensure PostgreSQL is running and DATABASE_URL is correctly configured."
            )
        raise HTTPException(status_code=500, detail=f"Error searching examples: {error_msg}")


@app.get(
    "/api/examples/{id}",
    tags=["Examples"],
    operation_id="apiExamplesIdGet",
    response_model=ExampleResponse,
    summary="Get example by ID",
    description="Retrieves a specific example by its ID"
)
async def get_example_by_id(id: int, db: Session = Depends(get_db)):
    """
    Get example by ID
    
    Returns a specific example if found, otherwise returns 404
    """
    try:
        example = db.query(Example).filter(Example.id == id).first()
        if not example:
            raise HTTPException(status_code=404, detail=f"Example with ID {id} not found")
        return example
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower() or "could not connect" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Database connection failed. Please ensure PostgreSQL is running and DATABASE_URL is correctly configured."
            )
        raise HTTPException(status_code=500, detail=f"Error fetching example: {error_msg}")


@app.post(
    "/api/examples",
    tags=["Examples"],
    operation_id="apiExamplesPost",
    response_model=ExampleResponse,
    status_code=201,
    summary="Create a new example",
    description="Creates a new example record"
)
async def create_example(example_data: CreateExampleDto, db: Session = Depends(get_db)):
    """
    Create a new example
    
    Creates a new example with the provided data. Name and title are required.
    """
    try:
        # Validate required fields
        if not example_data.name or not example_data.name.strip():
            raise HTTPException(status_code=400, detail="Name is required")
        if not example_data.title or not example_data.title.strip():
            raise HTTPException(status_code=400, detail="Title is required")
        
        # Create new example
        new_example = Example(
            name=example_data.name.strip(),
            title=example_data.title.strip(),
            description=example_data.description.strip() if example_data.description else None,
            is_active=example_data.isActive if example_data.isActive is not None else True,
        )
        
        db.add(new_example)
        db.commit()
        db.refresh(new_example)
        
        return new_example
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower() or "could not connect" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Database connection failed. Please ensure PostgreSQL is running and DATABASE_URL is correctly configured."
            )
        raise HTTPException(status_code=400, detail=f"Error creating example: {error_msg}")


@app.put(
    "/api/examples/{id}",
    tags=["Examples"],
    operation_id="apiExamplesIdPut",
    response_model=ExampleResponse,
    summary="Update an example",
    description="Updates an existing example record (partial updates supported)"
)
async def update_example(id: int, example_data: UpdateExampleDto, db: Session = Depends(get_db)):
    """
    Update an example
    
    Updates an existing example. All fields are optional (partial updates).
    """
    try:
        # Find existing example
        example = db.query(Example).filter(Example.id == id).first()
        if not example:
            raise HTTPException(status_code=404, detail=f"Example with ID {id} not found")
        
        # Update fields if provided
        if example_data.name is not None:
            if not example_data.name.strip():
                raise HTTPException(status_code=400, detail="Name cannot be empty")
            example.name = example_data.name.strip()
        
        if example_data.title is not None:
            if not example_data.title.strip():
                raise HTTPException(status_code=400, detail="Title cannot be empty")
            example.title = example_data.title.strip()
        
        if example_data.description is not None:
            example.description = example_data.description.strip() if example_data.description.strip() else None
        
        if example_data.isActive is not None:
            example.is_active = example_data.isActive
        
        db.commit()
        db.refresh(example)
        
        return example
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower() or "could not connect" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Database connection failed. Please ensure PostgreSQL is running and DATABASE_URL is correctly configured."
            )
        raise HTTPException(status_code=400, detail=f"Error updating example: {error_msg}")


@app.delete(
    "/api/examples/{id}",
    tags=["Examples"],
    operation_id="apiExamplesIdDelete",
    status_code=204,
    summary="Delete an example",
    description="Deletes an example record"
)
async def delete_example(id: int, db: Session = Depends(get_db)):
    """
    Delete an example
    
    Deletes an example by ID. Returns 204 No Content on success.
    """
    try:
        # Find existing example
        example = db.query(Example).filter(Example.id == id).first()
        if not example:
            raise HTTPException(status_code=404, detail=f"Example with ID {id} not found")
        
        db.delete(example)
        db.commit()
        
        return Response(status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower() or "could not connect" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Database connection failed. Please ensure PostgreSQL is running and DATABASE_URL is correctly configured."
            )
        raise HTTPException(status_code=500, detail=f"Error deleting example: {error_msg}")


# Graceful shutdown handlers
def handle_shutdown(signum, frame):
    """Handle graceful shutdown on SIGTERM/SIGINT"""
    print(f"\n{'SIGTERM' if signum == signal.SIGTERM else 'SIGINT'} signal received: closing server")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


if __name__ == "__main__":

    print(f"Server is running on http://localhost:{PORT}")
    print(f"Swagger UI available at http://localhost:{PORT}/api/swagger")
    print(f"OpenAPI JSON available at http://localhost:{PORT}/api/openapi.json")
    print(f"OpenAPI YAML available at http://localhost:{PORT}/api/openapi.yaml")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    )