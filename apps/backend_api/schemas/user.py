from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime

class UserPreferenceBase(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    preferred_locations: Optional[List[str]] = None
    min_bedrooms: Optional[int] = None

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreference(UserPreferenceBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
