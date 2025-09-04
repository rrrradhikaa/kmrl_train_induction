# kmrl_train_induction/api/schemas.py
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Small helper so SQLAlchemy objects can be converted to Pydantic easily
class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# FitnessCertificate schemas
# ---------------------------
class FitnessCertificateBase(BaseModel):
    train_id: str
    coach_id: str
    fitness_check_date: date
    fitness_status: Optional[str] = None
    defects_found: Optional[str] = None
    issued_by: Optional[str] = None
    valid_till: Optional[date] = None
    odometer_km: Optional[int] = None
    remarks: Optional[str] = None

class FitnessCertificateCreate(FitnessCertificateBase):
    # In your models certificate_id is the PK (string)
    certificate_id: str

class FitnessCertificateUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    fitness_check_date: Optional[date] = None
    fitness_status: Optional[str] = None
    defects_found: Optional[str] = None
    issued_by: Optional[str] = None
    valid_till: Optional[date] = None
    odometer_km: Optional[int] = None
    remarks: Optional[str] = None

class FitnessCertificateOut(ORMModel, FitnessCertificateBase):
    certificate_id: str


# ---------------------------
# JobCard schemas
# ---------------------------
class JobCardBase(BaseModel):
    train_id: str
    coach_id: str
    task: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    scheduled_date: Optional[datetime] = None

class JobCardCreate(JobCardBase):
    job_id: str

class JobCardUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    task: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    scheduled_date: Optional[datetime] = None

class JobCardOut(ORMModel, JobCardBase):
    job_id: str


# ---------------------------
# BrandingPriority schemas
# ---------------------------
class BrandingPriorityBase(BaseModel):
    train_id: str
    coach_id: str
    brand_task: Optional[str] = None
    priority: Optional[str] = None   # model uses String; if you change model -> int, update here
    deadline: Optional[date] = None
    owner_team: Optional[str] = None

class BrandingPriorityCreate(BrandingPriorityBase):
    pass  # id is autoincrement in model, don't provide

class BrandingPriorityUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    brand_task: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[date] = None
    owner_team: Optional[str] = None

class BrandingPriorityOut(ORMModel, BrandingPriorityBase):
    id: int


# ---------------------------
# MileageBalancing schemas
# ---------------------------
class MileageBalancingBase(BaseModel):
    train_id: str
    coach_id: str
    odometer_km: Optional[int] = None
    balance_action: Optional[str] = None
    next_due_km: Optional[int] = None
    remarks: Optional[str] = None

class MileageBalancingCreate(MileageBalancingBase):
    pass  # id is autoincrement

class MileageBalancingUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    odometer_km: Optional[int] = None
    balance_action: Optional[str] = None
    next_due_km: Optional[int] = None
    remarks: Optional[str] = None

class MileageBalancingOut(ORMModel, MileageBalancingBase):
    id: int


# ---------------------------
# CleaningSlot schemas
# ---------------------------
class CleaningSlotBase(BaseModel):
    train_id: str
    coach_id: str
    location: Optional[str] = None
    cleaning_time: Optional[datetime] = None
    cleaning_type: Optional[str] = None
    assigned_cleaner: Optional[str] = None

class CleaningSlotCreate(CleaningSlotBase):
    slot_id: str  # your model uses slot_id as PK

class CleaningSlotUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    location: Optional[str] = None
    cleaning_time: Optional[datetime] = None
    cleaning_type: Optional[str] = None
    assigned_cleaner: Optional[str] = None

class CleaningSlotOut(ORMModel, CleaningSlotBase):
    slot_id: str


# ---------------------------
# StablingGeometry schemas
# ---------------------------
class StablingGeometryBase(BaseModel):
    train_id: str
    coach_id: str
    length_m: Optional[int] = None
    width_m: Optional[int] = None
    height_m: Optional[int] = None
    yard_location: Optional[str] = None

class StablingGeometryCreate(StablingGeometryBase):
    stable_id: str  # PK

class StablingGeometryUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    length_m: Optional[int] = None
    width_m: Optional[int] = None
    height_m: Optional[int] = None
    yard_location: Optional[str] = None

class StablingGeometryOut(ORMModel, StablingGeometryBase):
    stable_id: str
