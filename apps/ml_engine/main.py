from fastapi import FastAPI, HTTPException
from .engine import recommender
from .utils import fetch_house_listings, fetch_user_preferences

app = FastAPI(title="Smart House ML Recommendation Engine")

@app.get("/")
async def root():
    return {"message": "Smart House ML Recommendation Engine is running"}

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: int):
    from .utils import fetch_user_interactions
    # 1. Fetch user preferences
    prefs = fetch_user_preferences(user_id)
    if not prefs:
        prefs = {"user_id": user_id, "min_price": 100000, "max_price": 500000, "min_bedrooms": 2} # Default for cold start
        
    # 2. Fetch all listings
    listings = fetch_house_listings()
    if not listings:
        return {"user_id": user_id, "recommendations": [], "message": "No listings available"}
        
    # 3. Fetch interactions for collaborative filtering
    interactions = fetch_user_interactions()
    
    # 4. Generate hybrid recommendations
    recommendations = recommender.recommend(prefs, listings, interactions=interactions)
    
    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "engine": "Hybrid (Content + Collaborative)"
    }
