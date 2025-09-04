from typing import Generator
from fastapi import Depends
from kmrl_train_induction.mock_api.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS helper (use in main)
def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # dev me open rakho; prod me restrict karo
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
