from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from ..database import get_db, SQLALCHEMY_DATABASE_URL
from ..models.interaction import UserInteraction
from ..models.house import HouseListing
from ..models.user import User

router = APIRouter(prefix="/analytics", tags=["analytics"])

def _is_sqlite():
    return SQLALCHEMY_DATABASE_URL.startswith("sqlite")

def _day_filter(query, model_col, day: date):
    """Portable date-filter for SQLite and PostgreSQL."""
    if _is_sqlite():
        day_str = day.strftime("%Y-%m-%d")
        return query.filter(func.strftime("%Y-%m-%d", model_col) == day_str)
    else:
        from sqlalchemy import cast, Date
        return query.filter(func.cast(model_col, Date) == day)


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """Returns high-level KPI totals for the dashboard."""
    total_users         = db.query(func.count(User.id)).scalar() or 0
    total_interactions  = db.query(func.count(UserInteraction.id)).scalar() or 0

    today_q = db.query(func.count(UserInteraction.id))
    active_today = _day_filter(today_q, UserInteraction.created_at, date.today()).scalar() or 0

    click_count  = db.query(func.count(UserInteraction.id)).filter(UserInteraction.event_type == "click").scalar() or 0
    save_count   = db.query(func.count(UserInteraction.id)).filter(UserInteraction.event_type == "save").scalar() or 0
    search_count = db.query(func.count(UserInteraction.id)).filter(UserInteraction.event_type == "search").scalar() or 0
    ctr = round((click_count / total_interactions * 100), 1) if total_interactions > 0 else 0.0

    return {
        "total_users":        total_users,
        "total_interactions": total_interactions,
        "active_today":       active_today,
        "click_count":        click_count,
        "save_count":         save_count,
        "search_count":       search_count,
        "click_through_rate": ctr
    }


@router.get("/interactions/daily")
def get_daily_interactions(db: Session = Depends(get_db)):
    """Returns click/save/search counts per day for the last 7 days."""
    result = []
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        def day_type_count(etype):
            q = db.query(func.count(UserInteraction.id)).filter(UserInteraction.event_type == etype)
            return _day_filter(q, UserInteraction.created_at, day).scalar() or 0

        result.append({
            "date":    str(day),
            "clicks":  day_type_count("click"),
            "saves":   day_type_count("save"),
            "searches":day_type_count("search"),
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
        house = db.query(HouseListing).filter(HouseListing.id == house_id).first()
        if house:
            result.append({
                "house_id":  house_id,
                "title":     house.title,
                "location":  house.location,
                "engagement":engagement
            })
    return result
