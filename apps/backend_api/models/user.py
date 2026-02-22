from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    preferences = relationship("UserPreference", back_populates="user", uselist=False)

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    preferred_locations = Column(JSON, nullable=True)
    min_bedrooms = Column(Integer, nullable=True)
    
    user = relationship("User", back_populates="preferences")
