from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Train(Base):
    __tablename__ = "trains"
    
    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String(10), unique=True, nullable=False, index=True)
    current_mileage = Column(Integer, default=0)
    last_maintenance_date = Column(Date)
    maintenance_interval = Column(Integer, default=90)
    equipment_status = Column(String(20), default="operational")  
    status = Column(String(20), default="active")
    
    # Relationships
    fitness_certificates = relationship("FitnessCertificate", back_populates="train")
    job_cards = relationship("JobCard", back_populates="train")
    branding_contracts = relationship("BrandingContract", back_populates="train")
    cleaning_slots = relationship("CleaningSlot", back_populates="train")
    stabling_geometry = relationship("StablingGeometry", back_populates="train")
    induction_plans = relationship("InductionPlan", back_populates="train")

class FitnessCertificate(Base):
    __tablename__ = "fitness_certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    department = Column(String(50), nullable=False)  # Rolling-Stock, Signalling, Telecom
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=False)
    is_valid = Column(Boolean, default=True)
    
    train = relationship("Train", back_populates="fitness_certificates")

class JobCard(Base):
    __tablename__ = "job_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    work_order_id = Column(String(100), nullable=False)
    status = Column(String(20), default="open")  # open, closed
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True))
    
    train = relationship("Train", back_populates="job_cards")

class BrandingContract(Base):
    __tablename__ = "branding_contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    advertiser_name = Column(String(100))
    contract_value = Column(Float, default=0.0)
    exposure_hours_required = Column(Integer)
    exposure_hours_fulfilled = Column(Integer, default=0)
    start_date = Column(Date)
    end_date = Column(Date)
    
    train = relationship("Train", back_populates="branding_contracts")

class CleaningSlot(Base):
    __tablename__ = "cleaning_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    slot_time = Column(DateTime(timezone=True))
    bay_number = Column(Integer)
    manpower_required = Column(Integer)
    status = Column(String(20), default="scheduled")  # scheduled, completed, cancelled
    
    train = relationship("Train", back_populates="cleaning_slots")

class StablingGeometry(Base):
    __tablename__ = "stabling_geometry"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    bay_position = Column(String(10))
    stabled_at = Column(DateTime(timezone=True), server_default=func.now())
    shunting_required = Column(Boolean, default=False)
    
    train = relationship("Train", back_populates="stabling_geometry")

class InductionPlan(Base):
    __tablename__ = "induction_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_date = Column(Date, nullable=False)
    train_id = Column(Integer, ForeignKey("trains.id"))
    induction_type = Column(String(20))  # service, standby, maintenance
    rank = Column(Integer)
    reason = Column(Text)
    approved_by = Column(Integer)  # user_id
    approved_at = Column(DateTime(timezone=True))
    
    train = relationship("Train", back_populates="induction_plans")

class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    feedback_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20))  # operator, supervisor, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())