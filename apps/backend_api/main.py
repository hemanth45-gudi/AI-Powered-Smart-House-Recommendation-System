from fastapi import FastAPI
from .routers import houses, users, interactions, analytics, seed
from .database import engine, Base

# Auto-create all tables on startup (SQLite / PostgreSQL)
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart House Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(houses.router)
app.include_router(users.router)
app.include_router(interactions.router)
app.include_router(analytics.router)
app.include_router(seed.router)

@app.on_event("startup")
def startup_event():
    """Seeds the database on first run if it's empty."""
    from .database import SessionLocal
    from .models.house import HouseListing
    from .routers.seed import seed_data
    
    db = SessionLocal()
    try:
        count = db.query(HouseListing).count()
        if count == 0:
            print("[Startup] Database empty. Seeding sample houses...")
            seed_data(clear=False, db=db)
    except Exception as e:
        print(f"[Startup Error] {e}")
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart House Recommendation API"}
