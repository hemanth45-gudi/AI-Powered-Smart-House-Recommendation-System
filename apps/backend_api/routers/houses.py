from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import house as models
from ..schemas import house as schemas

router = APIRouter(
    prefix="/houses",
    tags=["houses"]
)

from sqlalchemy.exc import IntegrityError

@router.post("/", response_model=schemas.HouseListing)
def create_house(house: schemas.HouseListingCreate, db: Session = Depends(get_db)):
    db_house = models.HouseListing(**house.model_dump())
    db.add(db_house)
    try:
        db.commit()
        db.refresh(db_house)
        return db_house
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A house with this title, location, and price already exists.")

@router.get("/", response_model=List[schemas.HouseListing])
def read_houses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    houses = db.query(models.HouseListing).offset(skip).limit(limit).all()
    return houses

@router.get("/{house_id}", response_model=schemas.HouseListing)
def read_house(house_id: int, db: Session = Depends(get_db)):
    db_house = db.query(models.HouseListing).filter(models.HouseListing.id == house_id).first()
    if db_house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return db_house
