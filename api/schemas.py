from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional

# -----------------------------
# Utility Validators
# -----------------------------
def parse_date(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in DD-MM-YYYY format")
    return value

def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%d-%m-%Y")
    return value

def parse_datetime(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%d-%m-%Y %H:%M")
        except ValueError:
            raise ValueError("Datetime must be in DD-MM-YYYY HH:MM format")
    return value

def format_datetime(value):
    if isinstance(value, datetime):
        return value.strftime("%d-%m-%Y %H:%M")
    return value

# -----------------------------
# Fitness Certificates
# -----------------------------
class FitnessCertificateBase(BaseModel):
    train_id: str
    coach_id: str
    fitness_check_date: date
    fitness_status: str
    defects_found: Optional[str] = None
    issued_by: Optional[str] = None
    valid_till: Optional[date] = None
    odometer_km: Optional[int] = None
    remarks: Optional[str] = None

    @field_validator("fitness_check_date", mode="before")
    def _parse_fitness_check_date(cls, v):
        return parse_date(v)

    @field_validator("valid_till", mode="before")
    def _parse_valid_till(cls, v):
        return parse_date(v)

class FitnessCertificateCreate(FitnessCertificateBase):
    certificate_id: str

class FitnessCertificate(FitnessCertificateBase):
    certificate_id: str

    @field_validator("fitness_check_date", mode="after")
    def _format_fitness_check_date(cls, v):
        return format_date(v)

    @field_validator("valid_till", mode="after")
    def _format_valid_till(cls, v):
        return format_date(v)

    model_config = dict(from_attributes=True)

# PATCH schema
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

    @field_validator("fitness_check_date", mode="before")
    def _parse_fitness_check_date(cls, v):
        return parse_date(v)

    @field_validator("valid_till", mode="before")
    def _parse_valid_till(cls, v):
        return parse_date(v)


# -----------------------------
# Job Cards
# -----------------------------
class JobCardBase(BaseModel):
    train_id: str
    coach_id: str
    task: str
    status: str
    assigned_to: str
    scheduled_date: datetime

    @field_validator("scheduled_date", mode="before")
    def _parse_scheduled_date(cls, v):
        return parse_datetime(v)

class JobCardCreate(JobCardBase):
    job_id: str

class JobCard(JobCardBase):
    job_id: str

    @field_validator("scheduled_date", mode="after")
    def _format_scheduled_date(cls, v):
        return format_datetime(v)

    model_config = dict(from_attributes=True)

class JobCardUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    task: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    scheduled_date: Optional[datetime] = None

    @field_validator("scheduled_date", mode="before")
    def _parse_scheduled_date(cls, v):
        return parse_datetime(v)


# -----------------------------
# Branding Priorities
# -----------------------------
class BrandingPriorityBase(BaseModel):
    train_id: str
    coach_id: str
    brand_task: str
    priority: str
    deadline: date
    owner_team: str

    @field_validator("deadline", mode="before")
    def _parse_deadline(cls, v):
        return parse_date(v)

class BrandingPriorityCreate(BrandingPriorityBase):
    pass

class BrandingPriority(BrandingPriorityBase):
    id: int

    @field_validator("deadline", mode="after")
    def _format_deadline(cls, v):
        return format_date(v)

    model_config = dict(from_attributes=True)

class BrandingPriorityUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    brand_task: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[date] = None
    owner_team: Optional[str] = None

    @field_validator("deadline", mode="before")
    def _parse_deadline(cls, v):
        return parse_date(v)


# -----------------------------
# Mileage Balancing
# -----------------------------
class MileageBalancingBase(BaseModel):
    train_id: str
    coach_id: str
    odometer_km: int
    balance_action: str
    next_due_km: int
    remarks: str

class MileageBalancingCreate(MileageBalancingBase):
    pass

class MileageBalancing(MileageBalancingBase):
    id: int
    model_config = dict(from_attributes=True)

class MileageBalancingUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    odometer_km: Optional[int] = None
    balance_action: Optional[str] = None
    next_due_km: Optional[int] = None
    remarks: Optional[str] = None


# -----------------------------
# Cleaning Slots
# -----------------------------
class CleaningSlotBase(BaseModel):
    train_id: str
    coach_id: str
    location: str
    cleaning_time: datetime
    cleaning_type: str
    assigned_cleaner: str

    @field_validator("cleaning_time", mode="before")
    def _parse_cleaning_time(cls, v):
        return parse_datetime(v)

class CleaningSlotCreate(CleaningSlotBase):
    slot_id: str

class CleaningSlot(CleaningSlotBase):
    slot_id: str

    @field_validator("cleaning_time", mode="after")
    def _format_cleaning_time(cls, v):
        return format_datetime(v)

    model_config = dict(from_attributes=True)

class CleaningSlotUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    location: Optional[str] = None
    cleaning_time: Optional[datetime] = None
    cleaning_type: Optional[str] = None
    assigned_cleaner: Optional[str] = None

    @field_validator("cleaning_time", mode="before")
    def _parse_cleaning_time(cls, v):
        return parse_datetime(v)


# -----------------------------
# Stabling Geometry
# -----------------------------
class StablingGeometryBase(BaseModel):
    train_id: str
    coach_id: str
    length_m: int
    width_m: int
    height_m: int
    yard_location: str

class StablingGeometryCreate(StablingGeometryBase):
    stable_id: str

class StablingGeometry(StablingGeometryBase):
    stable_id: str
    model_config = dict(from_attributes=True)

class StablingGeometryUpdate(BaseModel):
    train_id: Optional[str] = None
    coach_id: Optional[str] = None
    length_m: Optional[int] = None
    width_m: Optional[int] = None
    height_m: Optional[int] = None
    yard_location: Optional[str] = None
