from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.house import HouseListing
from ..models.user import User
from ..models.interaction import UserInteraction
import random

router = APIRouter(prefix="/seed", tags=["seed"])

@router.api_route("/", methods=["GET", "POST"])
def seed_data(db: Session = Depends(get_db)):
    """Seeds the database with houses, users, and interactions for testing."""
    # 1. Clear existing (optional, but good for clean testing)
    db.query(UserInteraction).delete()
    db.query(HouseListing).delete()
    db.query(User).delete()
    db.commit()

    # 2. Add Houses
    locations = ["Downtown", "Suburbs", "Uptown", "Beachfront", "Mountain View"]
    houses = []
    for i in range(1, 21):
        h = HouseListing(
            title=f"Modern House {i}",
            description=f"Beautiful home in {random.choice(locations)}",
            price=random.randint(200000, 800000),
            location=random.choice(locations),
            bedrooms=random.randint(1, 5),
            bathrooms=random.randint(1, 3),
            sqft=random.randint(1000, 3500)
        )
        db.add(h)
        houses.append(h)
    
    # 3. Add Users
    users = []
    for i in range(1, 6):
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
    return {"message": "Database seeded successfully", "houses": 20, "users": 5, "interactions": 50}
