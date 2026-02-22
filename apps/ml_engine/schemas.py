from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class UserPreferenceRequest(BaseModel):
    user_id: Optional[int] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    preferred_location: Optional[str] = None
    preferred_locations: Optional[List[str]] = None
    min_bedrooms: Optional[int] = Field(None, ge=0)

class Explanation(BaseModel):
    reason: str
    top_matches: List[str]

class HouseRecommendation(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    sqft: Optional[int] = None
    score: Optional[float] = None
    content_match: Optional[float] = None
    collab_match: Optional[float] = None
    explanation: Optional[Explanation] = None

    model_config = {"extra": "allow"}  # allow extra DB fields

class RecommendationResponse(BaseModel):
    user_id: Optional[int] = None
    recommendations: List[HouseRecommendation]
    engine: str
    message: Optional[str] = None
