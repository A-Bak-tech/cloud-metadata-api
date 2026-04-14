"""
CRUD operations for cloud resource metadata
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def get_resource_by_id(db: Session, resource_id: str):
    """Retrieve a resource by its unique resource_id"""
    return db.query(models.Resource).filter(models.Resource.resource_id == resource_id).first()

def get_resources(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all resources with pagination"""
    return db.query(models.Resource).offset(skip).limit(limit).all()

def create_resource(db: Session, resource: schemas.ResourceCreate):
    """Create a new resource"""
    db_resource = models.Resource(
        resource_id=resource.resource_id,
        resource_type=resource.resource_type,
        region=resource.region,
        status=resource.status,
        tags=resource.tags
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def update_resource(db: Session, resource_id: str, resource: schemas.ResourceUpdate):
    """Update an existing resource"""
    db_resource = get_resource_by_id(db, resource_id)
    if db_resource:
        update_data = resource.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_resource, key, value)
        db.commit()
        db.refresh(db_resource)
    return db_resource

def delete_resource(db: Session, resource_id: str):
    """Delete a resource"""
    db_resource = get_resource_by_id(db, resource_id)
    if db_resource:
        db.delete(db_resource)
        db.commit()
    return db_resource

def get_resources_by_region(db: Session, region: str):
    """Retrieve all resources in a specific region"""
    return db.query(models.Resource).filter(models.Resource.region == region).all()

def get_resources_by_type(db: Session, resource_type: str):
    """Retrieve all resources of a specific type"""
    return db.query(models.Resource).filter(models.Resource.resource_type == resource_type).all()

def get_resources_by_status(db: Session, status: str):
    """Retrieve all resources with a specific status"""
    return db.query(models.Resource).filter(models.Resource.status == status).all()

def get_resource_stats(db: Session):
    """Get summary statistics about resources"""
    total_resources = db.query(models.Resource).count()
    
    resources_by_type = db.query(
        models.Resource.resource_type,
        func.count(models.Resource.id).label('count')
    ).group_by(models.Resource.resource_type).all()
    
    resources_by_region = db.query(
        models.Resource.region,
        func.count(models.Resource.id).label('count')
    ).group_by(models.Resource.region).all()
    
    resources_by_status = db.query(
        models.Resource.status,
        func.count(models.Resource.id).label('count')
    ).group_by(models.Resource.status).all()
    
    return {
        "total_resources": total_resources,
        "by_type": {item[0]: item[1] for item in resources_by_type},
        "by_region": {item[0]: item[1] for item in resources_by_region},
        "by_status": {item[0]: item[1] for item in resources_by_status}
    }