from fastapi import FastAPI

app = FastAPI(title="Smart House ML Recommendation Engine")

@app.get("/")
async def root():
    return {"message": "Smart House ML Recommendation Engine is running"}

@app.get("/recommend")
async def get_recommendations(user_id: str):
    # Placeholder for recommendation logic
    return {"user_id": user_id, "recommendations": []}
