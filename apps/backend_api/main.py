from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .routers import houses, users, interactions, analytics, seed, auth
from .database import engine, Base
import time
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

# Configure optimization and performance logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Auto-create all tables on startup (SQLite / PostgreSQL)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart House Recommendation API")

# Mount rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"[Global Exception] {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error. Our engineers have been notified."})

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"[metrics] API Response Time: {request.method} {request.url.path} - {process_time:.4f}s")
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Strict CORS in Production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-production-frontend.com", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth.router)
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
