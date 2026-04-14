"""
Database models for cloud resource metadata
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class Resource(Base):
    """
    SQLAlchemy model for cloud resources.
    Tracks metadata and lifecycle information for cloud infrastructure.
    """
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String, unique=True, index=True, nullable=False)
    resource_type = Column(String, index=True, nullable=False)
    region = Column(String, index=True, nullable=False)
    status = Column(String, index=True, nullable=False, default="provisioning")
    tags = Column(JSON, nullable=True)  # Changed from 'metadata' to 'tags'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    def __repr__(self):
        return f"<Resource(resource_id='{self.resource_id}', type='{self.resource_type}', status='{self.status}')>"