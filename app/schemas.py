"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ResourceBase(BaseModel):
    """Base schema for resource data"""
    resource_id: str = Field(..., description="Unique identifier for the resource", example="vm-eastus-001")
    resource_type: str = Field(..., description="Type of cloud resource", example="virtual_machine")
    region: str = Field(..., description="Geographic region", example="eastus")
    status: str = Field(default="provisioning", description="Lifecycle status", example="active")
    tags: Optional[Dict[str, Any]] = Field(None, description="Additional key-value tags")

class ResourceCreate(ResourceBase):
    """Schema for creating a new resource"""
    pass

class ResourceUpdate(BaseModel):
    """Schema for updating an existing resource"""
    resource_type: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None

class Resource(ResourceBase):
    """Schema for resource response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True