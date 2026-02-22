from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from .engine import recommender
from .utils import fetch_house_listings, fetch_user_preferences, fetch_user_interactions
from .schemas import UserPreferenceRequest, RecommendationResponse
import json

app = FastAPI(title="Smart House ML Recommendation Engine")

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_recommendations(self, user_id: int, data: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_text(json.dumps(data))

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Smart House ML Recommendation Engine is running"}

@app.websocket("/ws/recommend/{user_id}")
async def websocket_recommend(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        # Push initial recommendations on connect
        prefs = fetch_user_preferences(user_id) or {
            "user_id": user_id, "min_price": 100000, "max_price": 500000, "min_bedrooms": 2
        }
        listings = fetch_house_listings() or []
        interactions = fetch_user_interactions()
        recommendations = recommender.recommend(prefs, listings, interactions=interactions)
        await manager.send_recommendations(user_id, {
            "event": "recommendations_updated",
            "engine": "Hybrid (Real-Time)",
            "count": len(recommendations),
            "recommendations": recommendations
        })
        # Listen for client refresh triggers
        while True:
            data = await websocket.receive_text()
            client_prefs = json.loads(data)
            listings = fetch_house_listings() or []
            interactions = fetch_user_interactions()
            recommendations = recommender.recommend(client_prefs, listings, interactions=interactions)
            await manager.send_recommendations(user_id, {
                "event": "recommendations_updated",
                "engine": "Hybrid (Real-Time)",
                "count": len(recommendations),
                "recommendations": recommendations
            })
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"User {user_id} disconnected from real-time feed.")

@app.get("/recommend/{user_id}", response_model=RecommendationResponse)
async def get_recommendations_by_profile(user_id: int):
    # 1. Fetch user preferences
    prefs = fetch_user_preferences(user_id)
    if not prefs:
        prefs = {"user_id": user_id, "min_price": 100000, "max_price": 500000, "min_bedrooms": 2}
        
    # 2. Fetch all listings
    listings = fetch_house_listings()
    if not listings:
        return {"user_id": user_id, "recommendations": [], "engine": "None", "message": "No listings available"}
        
    # 3. Fetch interactions for collaborative filtering
    interactions = fetch_user_interactions()
    
    # 4. Generate hybrid recommendations
    recommendations = recommender.recommend(prefs, listings, interactions=interactions)
    
    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "engine": "Hybrid (Content + Collaborative)"
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def get_adhoc_recommendations(prefs: UserPreferenceRequest):
    # 1. Fetch all listings
    listings = fetch_house_listings()
    if not listings:
        return {"recommendations": [], "engine": "None", "message": "No listings available"}
        
    # 2. Generate content-based recommendations (no interactions for ad-hoc/guest)
    recommendations = recommender.recommend(prefs.model_dump(), listings)
    
    return {
        "recommendations": recommendations,
        "engine": "Content-Based (Feature Similarity)"
    }
