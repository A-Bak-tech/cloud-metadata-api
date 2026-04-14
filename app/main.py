"""
Cloud Metadata API - Main Application
A RESTful API service for managing cloud resource metadata and lifecycle operations.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import crud, models, schemas
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Cloud Metadata API",
    description="RESTful API for managing cloud resource metadata and lifecycle operations",
    version="1.0.0"
)

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
    return {
        "status": "healthy",
        "service": "Cloud Metadata API",
        "version": "1.0.0"
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
    db_resource = crud.get_resource_by_id(db, resource_id=resource.resource_id)
    if db_resource:
        raise HTTPException(
            status_code=400,
            detail=f"Resource with ID '{resource.resource_id}' already exists"
        )
    return crud.create_resource(db=db, resource=resource)

@app.get("/resources/", response_model=List[schemas.Resource], tags=["Resources"])
def list_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all resources with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    resources = crud.get_resources(db, skip=skip, limit=limit)
    return resources

@app.get("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def get_resource(resource_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific resource by ID.
    
    - **resource_id**: The unique identifier of the resource
    """
    db_resource = crud.get_resource_by_id(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@app.put("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def update_resource(resource_id: str, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    """
    Update an existing resource's metadata or status.
    
    - **resource_id**: The unique identifier of the resource
    - **resource**: Updated resource data
    """
    db_resource = crud.get_resource_by_id(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return crud.update_resource(db=db, resource_id=resource_id, resource=resource)

@app.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Resources"])
def delete_resource(resource_id: str, db: Session = Depends(get_db)):
    """
    Delete a resource from the system.
    
    - **resource_id**: The unique identifier of the resource
    """
    db_resource = crud.get_resource_by_id(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    crud.delete_resource(db=db, resource_id=resource_id)
    return None

@app.get("/resources/region/{region}", response_model=List[schemas.Resource], tags=["Query"])
def get_resources_by_region(region: str, db: Session = Depends(get_db)):
    """
    Retrieve all resources in a specific region.
    
    - **region**: The geographic region to filter by
    """
    resources = crud.get_resources_by_region(db, region=region)
    return resources

@app.get("/resources/type/{resource_type}", response_model=List[schemas.Resource], tags=["Query"])
def get_resources_by_type(resource_type: str, db: Session = Depends(get_db)):
    """
    Retrieve all resources of a specific type.
    
    - **resource_type**: The type of resource to filter by
    """
    resources = crud.get_resources_by_type(db, resource_type=resource_type)
    return resources

@app.get("/resources/status/{status}", response_model=List[schemas.Resource], tags=["Query"])
def get_resources_by_status(status: str, db: Session = Depends(get_db)):
    """
    Retrieve all resources with a specific lifecycle status.
    
    - **status**: The lifecycle status to filter by (e.g., 'active', 'provisioning', 'terminated')
    """
    resources = crud.get_resources_by_status(db, status=status)
    return resources

@app.get("/stats/summary", tags=["Statistics"])
def get_summary_stats(db: Session = Depends(get_db)):
    """
    Get summary statistics about resources in the system.
    """
    return crud.get_resource_stats(db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)