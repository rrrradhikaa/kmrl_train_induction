from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from .database import Base

class FitnessCertificate(Base):
    __tablename__ = "fitness_certificates"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50))
    coach_id = Column(String(50))
    fitness_check_date = Column(Date)
    fitness_status = Column(String(20))
    defects_found = Column(String)
    certificate_id = Column(String(50))
    issued_by = Column(String(100))
    valid_till = Column(Date)
    odometer_km = Column(Integer)
    remarks = Column(String)

class JobCard(Base):
    __tablename__ = "job_cards"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50))
    coach_id = Column(String(50))
    job_id = Column(String(50))
    task = Column(String)
    status = Column(String)
    assigned_to = Column(String(100))
    scheduled_date = Column(DateTime)

class BrandingPriority(Base):
    __tablename__ = "branding_priorities"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50))
    coach_id = Column(String(50))
    brand_task = Column(String)
    priority = Column(String)
    deadline = Column(Date)
    owner_team = Column(String(100))

class MileageBalancing(Base):
    __tablename__ = "mileage_balancing"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50))
    coach_id = Column(String(50))
    odometer_km = Column(Integer)
    balance_action = Column(String)
    next_due_km = Column(Integer)
    remarks = Column(String)

class CleaningSlot(Base):
    __tablename__ = "cleaning_slots"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50))
    coach_id = Column(String(50))
    slot_id = Column(String(50))
    location = Column(String(100))
    cleaning_time = Column(DateTime)
    cleaning_type = Column(String)
    assigned_cleaner = Column(String(100))

class StablingGeometry(Base):
    __tablename__ = "stabling_geometry"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50))
    coach_id = Column(String(50))
    stable_id = Column(String(50))
    length_m = Column(Integer)
    width_m = Column(Integer)
    height_m = Column(Integer)
    yard_location = Column(String(100))