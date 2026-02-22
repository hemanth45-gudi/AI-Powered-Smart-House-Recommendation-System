from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class HouseListingBase(BaseModel):
    title: str
    description: str
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    sqft: int
    embedding_id: Optional[str] = None

class HouseListingCreate(HouseListingBase):
    pass

class HouseListing(HouseListingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
