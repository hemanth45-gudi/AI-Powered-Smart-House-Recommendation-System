from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import user as models
from ..security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Standard username mapping to user ID or email. 
    # For demo structure, assuming username is the User ID directly for lookup.
    try:
        user_id = int(form_data.username)
    except ValueError:
        raise HTTPException(status_code=400, detail="Username must be a valid User ID integer")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # If user doesn't exist, we dynamically create one matching the old behavior,
    # but strictly encrypting their password.
    if not user:
        hashed_pw = get_password_hash(form_data.password)
        user = models.User(id=user_id, email=f"user{user_id}@example.com", hashed_password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
        
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
