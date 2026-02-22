from pydantic import BaseModel, Field
from typing import List, Optional

class UserPreferenceRequest(BaseModel):
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    preferred_location: Optional[str] = None
    min_bedrooms: Optional[int] = Field(None, ge=0)

class HouseRecommendation(BaseModel):
    id: int
    title: str
    location: str
    price: float
    bedrooms: int
    bathrooms: int
    sqft: int
    score: float
    content_match: Optional[float] = None
    behavior_match: Optional[float] = None

class RecommendationResponse(BaseModel):
    user_id: Optional[int] = None
    recommendations: List[HouseRecommendation]
    engine: str
