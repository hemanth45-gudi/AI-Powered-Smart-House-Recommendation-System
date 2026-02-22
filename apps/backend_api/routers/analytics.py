from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import date, timedelta
from ..database import get_db
from ..models.interaction import UserInteraction
from ..models.house import House
from ..models.user import User

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """Returns high-level KPI totals for the dashboard."""
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_interactions = db.query(func.count(UserInteraction.id)).scalar() or 0
    today_interactions = db.query(func.count(UserInteraction.id)).filter(
        cast(UserInteraction.created_at, Date) == date.today()
    ).scalar() or 0
    click_count = db.query(func.count(UserInteraction.id)).filter(
        UserInteraction.interaction_type == "click"
    ).scalar() or 0
    save_count = db.query(func.count(UserInteraction.id)).filter(
        UserInteraction.interaction_type == "save"
    ).scalar() or 0
    search_count = db.query(func.count(UserInteraction.id)).filter(
        UserInteraction.interaction_type == "search"
    ).scalar() or 0
    ctr = round((click_count / total_interactions * 100), 1) if total_interactions > 0 else 0.0

    return {
        "total_users": total_users,
        "total_interactions": total_interactions,
        "active_today": today_interactions,
        "click_count": click_count,
        "save_count": save_count,
        "search_count": search_count,
        "click_through_rate": ctr
    }

@router.get("/interactions/daily")
def get_daily_interactions(db: Session = Depends(get_db)):
    """Returns interaction counts per day for the last 7 days, by type."""
    result = []
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        clicks = db.query(func.count(UserInteraction.id)).filter(
            cast(UserInteraction.created_at, Date) == day,
            UserInteraction.interaction_type == "click"
        ).scalar() or 0
        saves = db.query(func.count(UserInteraction.id)).filter(
            cast(UserInteraction.created_at, Date) == day,
            UserInteraction.interaction_type == "save"
        ).scalar() or 0
        searches = db.query(func.count(UserInteraction.id)).filter(
            cast(UserInteraction.created_at, Date) == day,
            UserInteraction.interaction_type == "search"
        ).scalar() or 0
        result.append({
            "date": str(day),
            "clicks": clicks,
            "saves": saves,
            "searches": searches
        })
    return result

@router.get("/top-houses")
def get_top_houses(db: Session = Depends(get_db)):
    """Returns the top 10 most interacted-with houses."""
    top = (
        db.query(
            UserInteraction.house_id,
            func.count(UserInteraction.id).label("engagement")
        )
        .filter(UserInteraction.house_id.isnot(None))
        .group_by(UserInteraction.house_id)
        .order_by(func.count(UserInteraction.id).desc())
        .limit(10)
        .all()
    )
    result = []
    for house_id, engagement in top:
        house = db.query(House).filter(House.id == house_id).first()
        if house:
            result.append({
                "house_id": house_id,
                "title": house.title,
                "location": house.location,
                "engagement": engagement
            })
    return result
