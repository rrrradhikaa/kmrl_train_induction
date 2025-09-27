from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

# Train Schemas
class TrainBase(BaseModel):
    train_number: str
    current_mileage: int = 0
    last_maintenance_date: Optional[date] = None
    maintenance_interval: int = 90
    equipment_status: str = "operational"
    status: str = "active"

class TrainCreate(TrainBase):
    pass

class TrainResponse(TrainBase):
    id: int
    
    class Config:
        from_attributes = True

# Fitness Certificate Schemas
class FitnessCertificateBase(BaseModel):
    department: str
    valid_from: date
    valid_until: date
    is_valid: bool = True

class FitnessCertificateCreate(FitnessCertificateBase):
    train_id: int

class FitnessCertificateResponse(FitnessCertificateBase):
    id: int
    train_id: int
    
    class Config:
        from_attributes = True

# Job Card Schemas
class JobCardBase(BaseModel):
    work_order_id: str
    status: str = "open"
    description: Optional[str] = None

class JobCardCreate(JobCardBase):
    train_id: int

class JobCardResponse(JobCardBase):
    id: int
    train_id: int
    created_at: datetime
    closed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Branding Contract Schemas
class BrandingContractBase(BaseModel):
    advertiser_name: str
    contract_value: float = 0.0 
    exposure_hours_required: int
    exposure_hours_fulfilled: int = 0
    start_date: date
    end_date: date

class BrandingContractCreate(BrandingContractBase):
    train_id: int

class BrandingContractResponse(BrandingContractBase):
    id: int
    train_id: int
    
    class Config:
        from_attributes = True

# Cleaning Slot Schemas
class CleaningSlotBase(BaseModel):
    slot_time: datetime
    bay_number: int
    manpower_required: int
    status: str = "scheduled"

class CleaningSlotCreate(CleaningSlotBase):
    train_id: int

class CleaningSlotResponse(CleaningSlotBase):
    id: int
    train_id: int
    
    class Config:
        from_attributes = True

# Stabling Geometry Schemas
class StablingGeometryBase(BaseModel):
    bay_position: str
    shunting_required: bool = False

class StablingGeometryCreate(StablingGeometryBase):
    train_id: int

class StablingGeometryResponse(StablingGeometryBase):
    id: int
    train_id: int
    stabled_at: Optional[datetime]=None
    
    class Config:
        from_attributes = True

# Induction Plan Schemas
class InductionPlanBase(BaseModel):
    plan_date: date
    induction_type: str
    rank: int
    reason: Optional[str] = None

class InductionPlanCreate(InductionPlanBase):
    train_id: int

class InductionPlanResponse(InductionPlanBase):
    id: int
    train_id: int
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# User Feedback Schemas
class UserFeedbackBase(BaseModel):
    feedback_text: str

class UserFeedbackCreate(UserFeedbackBase):
    user_id: int

class UserFeedbackResponse(UserFeedbackBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chatbot Schemas
class ChatQuery(BaseModel):
    message: str
    user_id: Optional[int] = None

class WhatIfScenario(BaseModel):
    scenario_type: str
    parameters: str
    user_id: Optional[int] = None

# Data Upload Schemas
class WhatsAppUpload(BaseModel):
    messages: List[str]

class ManualDataUpload(BaseModel):
    trains: Optional[List[TrainCreate]] = None
    fitness_certificates: Optional[List[FitnessCertificateCreate]] = None
    job_cards: Optional[List[JobCardCreate]] = None
    branding_contracts: Optional[List[BrandingContractCreate]] = None

# Optimization Constraints Schema
class OptimizationConstraints(BaseModel):
    min_service_trains: int = 15
    max_service_trains: int = 20
    min_standby_trains: int = 3
    max_standby_trains: int = 5
    target_branding_exposure: float = 0.8
    max_mileage_variance: float = 0.2