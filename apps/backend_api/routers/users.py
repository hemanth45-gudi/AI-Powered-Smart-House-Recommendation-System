from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import user as models
from ..schemas import user as schemas

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{user_id}/preferences", response_model=schemas.UserPreference)
def update_preferences(user_id: int, prefs: schemas.UserPreferenceCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        db_user = models.User(id=user_id, email=f"user{user_id}@example.com", hashed_password="hashed")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    db_prefs = db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()
    if db_prefs:
        for key, value in prefs.model_dump().items():
            setattr(db_prefs, key, value)
    else:
        db_prefs = models.UserPreference(user_id=user_id, **prefs.model_dump())
        db.add(db_prefs)
    
    db.commit()
    db.refresh(db_prefs)
    return db_prefs

@router.get("/{user_id}/preferences", response_model=schemas.UserPreference)
def get_preferences(user_id: int, db: Session = Depends(get_db)):
    db_prefs = db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()
    if not db_prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return db_prefs
