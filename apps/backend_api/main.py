from fastapi import FastAPI
from .routers import houses, users, interactions

app = FastAPI(title="Smart House Recommendation API")

app.include_router(houses.router)
app.include_router(users.router)
app.include_router(interactions.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart House Recommendation API"}
