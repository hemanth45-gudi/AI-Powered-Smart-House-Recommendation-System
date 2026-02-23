from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.house import HouseListing
from ..models.user import User
from ..models.interaction import UserInteraction
import random

router = APIRouter(prefix="/seed", tags=["seed"])

@router.api_route("/", methods=["GET", "POST"])
def seed_data(clear: bool = False, db: Session = Depends(get_db)):
    """Seeds the database with houses, users, and interactions for testing."""    # 1. Clear existing (optional)
    if clear:
        db.query(UserInteraction).delete()
        db.query(HouseListing).delete()
        db.query(User).delete()
        db.commit()
    else:
        # Idempotency check: if not clearing and we already have 30 houses, skip
        count = db.query(HouseListing).count()
        if count >= 30:
            return {"message": "Database already seeded with 30+ houses. Use ?clear=True to reset.", "houses": count}

    # 2. Add Houses
    locations = ["Downtown", "Suburbs", "Uptown", "Beachfront", "Mountain View", "Nellore", "Ongole"]
    houses = []
    # Generate 30 houses as requested
    for i in range(1, 31):
        title = f"Premium Property {i}" if i > 25 else f"Modern House {i}"
        location = random.choice(locations)
        # Deterministic price: ensures idempotency check (Title+Loc+Price) is stable
        price = 200000 + (i * 50000)
        
        # Check if exists before adding (Idempotency)
        existing = db.query(HouseListing).filter(
            HouseListing.title == title,
            HouseListing.location == location,
            HouseListing.price == price
        ).first()
        
        if not existing:
            h = HouseListing(
                title=title,
                description=f"Beautiful home in {location}",
                price=price,
                location=location,
                bedrooms=random.randint(1, 6),
                bathrooms=random.randint(1, 4),
                sqft=random.randint(1000, 5000)
            )
            db.add(h)
            houses.append(h)
        else:
            houses.append(existing)
    
    # 3. Add Users
    users = []
    # Ensure tester users exist
    for i in range(1, 6):
        u = db.query(User).filter(User.email == f"tester{i}@example.com").first()
        if not u:
            u = User(email=f"tester{i}@example.com", hashed_password="hashed_password")
            db.add(u)
        users.append(u)
    
    db.commit()

    # 4. Add Interactions
    for u in users:
        for _ in range(10):
            h = random.choice(houses)
            interaction = UserInteraction(
                user_id=u.id,
                house_id=h.id,
                event_type=random.choice(["click", "save", "search"])
            )
            db.add(interaction)
    
    db.commit()

    total_houses = db.query(HouseListing).count()
    total_users = db.query(User).count()
    total_interactions = db.query(UserInteraction).count()

    return {
        "message": "Database seeded successfully", 
        "houses": total_houses, 
        "users": total_users, 
        "interactions": total_interactions
    }
