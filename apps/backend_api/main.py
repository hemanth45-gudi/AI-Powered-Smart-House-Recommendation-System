from fastapi import FastAPI
from .routers import houses, users, interactions, analytics, seed
from .database import engine, Base

# Auto-create all tables on startup (SQLite / PostgreSQL)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart House Recommendation API")

app.include_router(houses.router)
app.include_router(users.router)
app.include_router(interactions.router)
app.include_router(analytics.router)
app.include_router(seed.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart House Recommendation API"}
