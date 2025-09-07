from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    status = Column(String)  # Active, Delayed, Maintenance
    next_slot = Column(String)
    assigned_driver = Column(String)
    ai_confidence = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer)
    message = Column(String)
    severity = Column(String)  # Info, Warning, Critical
