from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.house import HouseListing
from ..models.user import User
from ..models.interaction import UserInteraction
import random

router = APIRouter(prefix="/seed", tags=["seed"])

@router.api_route("/", methods=["GET", "POST"])
def seed_data(clear: bool = True, db: Session = Depends(get_db)):
    """Seeds the database with houses, users, and interactions for testing."""
    # 1. Clear existing (optional)
    if clear:
        db.query(UserInteraction).delete()
        db.query(HouseListing).delete()
        db.query(User).delete()
        db.commit()

    # 2. Add Houses
    locations = ["Downtown", "Suburbs", "Uptown", "Beachfront", "Mountain View"]
    houses = []
    # Generate 30 houses as requested
    for i in range(1, 31):
        h = HouseListing(
            title=f"Premium Property {i}" if i > 20 else f"Modern House {i}",
            description=f"Beautiful home in {random.choice(locations)}",
            price=random.randint(200000, 2000000), # Broadened range to up to 2M
            location=random.choice(locations),
            bedrooms=random.randint(1, 6),
            bathrooms=random.randint(1, 4),
            sqft=random.randint(1000, 5000)
        )
        db.add(h)
        houses.append(h)
    
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
    return {"message": "Database seeded successfully", "houses": len(houses), "users": len(users), "interactions": len(users) * 10}
