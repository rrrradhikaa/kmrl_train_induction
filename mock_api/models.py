from sqlalchemy import Column, String, Integer, Date, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# -----------------------------
# Fitness Certificates
# -----------------------------
class FitnessCertificate(Base):
    __tablename__ = "fitness_certificates"

    certificate_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), nullable=False)
    coach_id = Column(String(50), nullable=False)
    fitness_check_date = Column(Date, nullable=False)
    fitness_status = Column(String(20), nullable=False)
    defects_found = Column(Text, nullable=True)
    issued_by = Column(String(100), nullable=True)
    valid_till = Column(Date, nullable=True)
    odometer_km = Column(Integer, nullable=True)
    remarks = Column(Text, nullable=True)


# -----------------------------
# Job Cards
# -----------------------------
class JobCard(Base):
    __tablename__ = "job_cards"

    job_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), nullable=False)
    coach_id = Column(String(50), nullable=False)
    task = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    assigned_to = Column(String(100), nullable=False)
    scheduled_date = Column(TIMESTAMP, nullable=False)


# -----------------------------
# Branding Priorities
# -----------------------------
class BrandingPriority(Base):
    __tablename__ = "branding_priorities"

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50), nullable=False)
    coach_id = Column(String(50), nullable=False)
    brand_task = Column(Text, nullable=False)
    priority = Column(Text, nullable=False)
    deadline = Column(Date, nullable=False)
    owner_team = Column(String(100), nullable=False)


# -----------------------------
# Mileage Balancing
# -----------------------------
class MileageBalancing(Base):
    __tablename__ = "mileage_balancing"

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(String(50), nullable=False)
    coach_id = Column(String(50), nullable=False)
    odometer_km = Column(Integer, nullable=False)
    balance_action = Column(Text, nullable=False)
    next_due_km = Column(Integer, nullable=False)
    remarks = Column(Text, nullable=False)


# -----------------------------
# Cleaning Slots
# -----------------------------
class CleaningSlot(Base):
    __tablename__ = "cleaning_slots"

    slot_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), nullable=False)
    coach_id = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    cleaning_time = Column(TIMESTAMP, nullable=False)
    cleaning_type = Column(Text, nullable=False)
    assigned_cleaner = Column(String(100), nullable=False)


# -----------------------------
# Stabling Geometry
# -----------------------------
class StablingGeometry(Base):
    __tablename__ = "stabling_geometry"

    stable_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), nullable=False)
    coach_id = Column(String(50), nullable=False)
    length_m = Column(Integer, nullable=False)
    width_m = Column(Integer, nullable=False)
    height_m = Column(Integer, nullable=False)
    yard_location = Column(String(100), nullable=False)
