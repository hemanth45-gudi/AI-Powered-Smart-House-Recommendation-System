from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.interaction import UserInteraction
from ..schemas.interaction import Interaction, InteractionCreate

router = APIRouter(
    prefix="/interactions",
    tags=["interactions"]
)

@router.post("/", response_model=Interaction)
def record_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    db_interaction = UserInteraction(**interaction.model_dump())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.get("/", response_model=list[Interaction])
def get_all_interactions(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    return db.query(UserInteraction).offset(skip).limit(limit).all()

@router.get("/user/{user_id}", response_model=list[Interaction])
def get_user_interactions(user_id: int, db: Session = Depends(get_db)):
    return db.query(UserInteraction).filter(UserInteraction.user_id == user_id).all()
