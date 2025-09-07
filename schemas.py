from pydantic import BaseModel
from typing import Optional

# --------------------
# Train Schemas
# --------------------
class TrainBase(BaseModel):
    name: str
    status: str
    next_slot: str
    assigned_driver: str
    ai_confidence: float

class TrainCreate(TrainBase):
    pass

class TrainUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    next_slot: Optional[str] = None
    assigned_driver: Optional[str] = None
    ai_confidence: Optional[float] = None

class TrainResponse(TrainBase):
    id: int
    class Config:
        orm_mode = True

# --------------------
# Alert Schemas
# --------------------
class AlertBase(BaseModel):
    train_id: int
    message: str
    severity: str

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    train_id: Optional[int] = None
    message: Optional[str] = None
    severity: Optional[str] = None

class AlertResponse(AlertBase):
    id: int
    class Config:
        orm_mode = True
