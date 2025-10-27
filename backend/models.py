"""Pydantic models for request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Optional

class ChatQuery(BaseModel):
    message: str = Field(..., description="User's natural language query")
    session_id: Optional[str] = Field(None, description="Session ID for context")

class PropertyCard(BaseModel):
    project_id: str
    title: str
    city: str
    locality: str
    bhk: str
    price: str
    price_raw: float
    project_name: str
    possession_status: str
    amenities: List[str]
    carpet_area: Optional[float] = None
    bathrooms: Optional[int] = None
    balconies: Optional[int] = None
    slug: str
    url: str

class ExtractedFilters(BaseModel):
    city: Optional[str] = None
    bhk: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    possession_status: Optional[str] = None
    locality: Optional[str] = None
    project_name: Optional[str] = None

class ChatResponse(BaseModel):
    summary: str = Field(..., description="AI-generated summary")
    properties: List[PropertyCard] = Field(..., description="List of matching properties")
    filters_applied: ExtractedFilters = Field(..., description="Filters extracted from query")
    total_results: int = Field(..., description="Total number of results found")
