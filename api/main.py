from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # 👈 import this
from .routers import (
    fitness_certificates,
    job_cards,
    branding_priorities,
    mileage_balancing,
    cleaning_slots,
    stabling_geometry,
    aggregate
)
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.mock_api.database import engine

# Create all tables (SQLAlchemy)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KMRL Train Induction API",
    description="API backend for train induction, scheduling, and maintenance modules",
    version="1.0.0"
)

# 👇 Add this block right after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 👈 your frontend
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, PUT, DELETE etc.
    allow_headers=["*"],  # allow all headers
)

# Routers
app.include_router(fitness_certificates.router)
app.include_router(job_cards.router)
app.include_router(branding_priorities.router)
app.include_router(mileage_balancing.router)
app.include_router(cleaning_slots.router)
app.include_router(stabling_geometry.router)
app.include_router(aggregate.router)

@app.get("/")
def root():
    return {"message": "🚆 Welcome to KMRL Train Induction API"}
