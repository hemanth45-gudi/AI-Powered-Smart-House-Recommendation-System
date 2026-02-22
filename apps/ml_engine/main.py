from fastapi import FastAPI, HTTPException
from .engine import recommender
from .utils import fetch_house_listings, fetch_user_preferences

app = FastAPI(title="Smart House ML Recommendation Engine")

@app.get("/")
async def root():
    return {"message": "Smart House ML Recommendation Engine is running"}

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: int):
    # 1. Fetch user preferences
    prefs = fetch_user_preferences(user_id)
    if not prefs:
        raise HTTPException(status_code=404, detail="User preferences not found")
        
    # 2. Fetch all listings
    listings = fetch_house_listings()
    if not listings:
        return {"user_id": user_id, "recommendations": [], "message": "No listings available"}
        
    # 3. Generate recommendations
    recommendations = recommender.recommend(prefs, listings)
    
    return {
        "user_id": user_id,
        "recommendations": recommendations
    }
