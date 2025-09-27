from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
import models

# Import all routers
from routers import (
    trains, fitness, job_cards, branding, cleaning, stabling, 
    induction, feedback, auth, ai, chatbot, data_upload, dashboard
)

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RailSpark - KMRL Train Induction System",
    description="AI-Driven Train Induction Planning & Scheduling for Kochi Metro",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(trains.router)
app.include_router(fitness.router)
app.include_router(job_cards.router)
app.include_router(branding.router)
app.include_router(cleaning.router)
app.include_router(stabling.router)
app.include_router(induction.router)
app.include_router(feedback.router)
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(chatbot.router)
app.include_router(data_upload.router)
app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {
        "message": "RailSpark - KMRL Train Induction System API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "RailSpark API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)