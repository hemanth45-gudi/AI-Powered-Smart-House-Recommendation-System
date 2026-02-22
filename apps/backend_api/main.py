from fastapi import FastAPI

app = FastAPI(title="Smart House Recommendation API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart House Recommendation API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
