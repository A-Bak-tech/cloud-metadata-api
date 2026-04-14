"""
Cloud Metadata API - Main Application
A RESTful API service for managing cloud resource metadata and lifecycle operations.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import logging
import time

from . import crud, models, schemas
from .database import SessionLocal, engine
from .logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Cloud Metadata API",
    description="RESTful API for managing cloud resource metadata and lifecycle operations",
    version="2.0.0"
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and their response times"""
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - Duration: {process_time:.3f}s")
    
    return response

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "Cloud Metadata API",
        "version": "2.0.0"
    }

@app.post("/resources/", response_model=schemas.Resource, status_code=status.HTTP_201_CREATED, tags=["Resources"])
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    """
    Create a new cloud resource with metadata.
    
    - **resource_id**: Unique identifier for the resource
    - **resource_type**: Type of resource (e.g., 'vm', 'storage', 'database')
    - **region**: Geographic region where resource is deployed
    - **status**: Current lifecycle status
    - **tags**: Additional key-value metadata
    """
    logger.info(f"Creating resource: {resource.resource_id}")
    db_resource = crud.get_resource_by_id(db, resource_id=resource.resource_id)
    if db_resource:
        logger.warning(f"Resource already exists: {resource.resource_id}")
        raise HTTPException(
            status_code=400,
            detail=f"Resource with ID '{resource.resource_id}' already exists"
        )
    created = crud.create_resource(db=db, resource=resource)
    logger.info(f"Resource created successfully: {resource.resource_id}")
    return created

@app.get("/resources/", response_model=List[schemas.Resource], tags=["Resources"])
def list_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all resources with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    logger.info(f"Listing resources: skip={skip}, limit={limit}")
    resources = crud.get_resources(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(resources)} resources")
    return resources

@app.get("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def get_resource(resource_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific resource by ID.
    
    - **resource_id**: The unique identifier of the resource
    """
    logger.info(f"Fetching resource: {resource_id}")
    db_resource = crud.get_resource_by_id(db, resource_id=resource_id)
    if db_resource is None:
        logger.warning(f"Resource not found: {resource_id}")
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@app.put("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def update_resource(resource_id: str, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    """
    Update an existing resource's metadata or status.
    
    - **resource_id**: The unique identifier of the resource
    - **resource**: Updated resource data
    """
    logger.info(f"Updating resource: {resource_id}")
    db_resource = crud.get_resource_by_id(db, resource_id=resource_id)
    if db_resource is None:
        logger.warning(f"Resource not found for update: {resource_id}")
        raise HTTPException(status_code=404, detail="Resource not found")
    updated = crud.update_resource(db=db, resource_id=resource_id, resource=resource)
    logger.info(f"Resource updated successfully: {resource_id}")
    return updated

@app.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Resources"])
def delete_resource(resource_id: str, db: Session = Depends(get_db)):
    """
    Delete a resource from the system.
    
    - **resource_id**: The unique identifier of the resource
    """
    logger.info(f"Deleting resource: {resource_id}")
    db_resource = crud.get_resource_by_id(db, resource_id=resource_id)
    if db_resource is None:
        logger.warning(f"Resource not found for deletion: {resource_id}")
        raise HTTPException(status_code=404, detail="Resource not found")
    crud.delete_resource(db=db, resource_id=resource_id)
    logger.info(f"Resource deleted successfully: {resource_id}")
    return None

@app.get("/resources/region/{region}", response_model=List[schemas.Resource], tags=["Query"])
def get_resources_by_region(region: str, db: Session = Depends(get_db)):
    """
    Retrieve all resources in a specific region.
    
    - **region**: The geographic region to filter by
    """
    logger.info(f"Querying resources by region: {region}")
    resources = crud.get_resources_by_region(db, region=region)
    logger.info(f"Found {len(resources)} resources in region {region}")
    return resources

@app.get("/resources/type/{resource_type}", response_model=List[schemas.Resource], tags=["Query"])
def get_resources_by_type(resource_type: str, db: Session = Depends(get_db)):
    """
    Retrieve all resources of a specific type.
    
    - **resource_type**: The type of resource to filter by
    """
    logger.info(f"Querying resources by type: {resource_type}")
    resources = crud.get_resources_by_type(db, resource_type=resource_type)
    logger.info(f"Found {len(resources)} resources of type {resource_type}")
    return resources

@app.get("/resources/status/{status}", response_model=List[schemas.Resource], tags=["Query"])
def get_resources_by_status(status: str, db: Session = Depends(get_db)):
    """
    Retrieve all resources with a specific lifecycle status.
    
    - **status**: The lifecycle status to filter by (e.g., 'active', 'provisioning', 'terminated')
    """
    logger.info(f"Querying resources by status: {status}")
    resources = crud.get_resources_by_status(db, status=status)
    logger.info(f"Found {len(resources)} resources with status {status}")
    return resources

@app.get("/stats/summary", tags=["Statistics"])
def get_summary_stats(db: Session = Depends(get_db)):
    """
    Get summary statistics about resources in the system.
    """
    logger.info("Generating resource statistics")
    stats = crud.get_resource_stats(db)
    return stats

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)