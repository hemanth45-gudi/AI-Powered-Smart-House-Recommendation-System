import os
from celery import Celery
import time
from .engine import recommender
import logging

logger = logging.getLogger(__name__)

# Initialize Celery app connected to Redis
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
app = Celery("ml_tasks", broker=broker_url, backend=broker_url)

@app.task(name="recalculate_all_user_preferences")
def recalculate_all_user_preferences():
    """
    Background worker task to simulate batch processing / cache warming 
    of all user recommendations without blocking the main event loop.
    """
    logger.info("[Celery Worker] Starting background cache warming for user recommendations...")
    start_time = time.time()
    
    # In a real scenario, this would loop through users from the DB 
    # and pre-calculate recommendations.
    time.sleep(2) # Simulating heavy CPU-bound matrix multiplication
    
    exec_time = time.time() - start_time
    logger.info(f"[Celery Worker] Cache warming complete. Took {exec_time:.2f}s")
    return {"status": "success", "duration_seconds": exec_time}
