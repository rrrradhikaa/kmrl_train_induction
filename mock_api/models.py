from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from kmrl_train_induction.mock_api.database import Base


# ---------------------------
# Fitness Certificates Table
# ---------------------------
class FitnessCertificate(Base):
    __tablename__ = "fitness_certificates"
    certificate_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), index=True)
    coach_id = Column(String(50))
    fitness_check_date = Column(Date)
    fitness_status = Column(String(20))
    defects_found = Column(String)
    issued_by = Column(String(100))
    valid_till = Column(Date)
    odometer_km = Column(Integer)
    remarks = Column(String)

# ---------------------------
# Job Cards Table
# ---------------------------
class JobCard(Base):
    __tablename__ = "job_cards"
    job_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), index=True)
    coach_id = Column(String(50))
    task = Column(String)
    status = Column(String)
    assigned_to = Column(String(100))
    scheduled_date = Column(DateTime)

# ---------------------------
# Branding Priorities Table
# ---------------------------
class BrandingPriority(Base):
    __tablename__ = "branding_priorities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    train_id = Column(String(50), index=True)
    coach_id = Column(String(50))
    brand_task = Column(String)
    priority = Column(String)
    deadline = Column(Date)
    owner_team = Column(String(100))

# ---------------------------
# Mileage Balancing Table
# ---------------------------
class MileageBalancing(Base):
    __tablename__ = "mileage_balancing"
    id = Column(Integer, primary_key=True, autoincrement=True)
    train_id = Column(String(50), index=True)
    coach_id = Column(String(50))
    odometer_km = Column(Integer)
    balance_action = Column(String)
    next_due_km = Column(Integer)
    remarks = Column(String)

# ---------------------------
# Cleaning Slots Table
# ---------------------------
class CleaningSlot(Base):
    __tablename__ = "cleaning_slots"
    slot_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), index=True)
    coach_id = Column(String(50))
    location = Column(String(100))
    cleaning_time = Column(DateTime)
    cleaning_type = Column(String)
    assigned_cleaner = Column(String(100))

# ---------------------------
# Stabling Geometry Table
# ---------------------------
class StablingGeometry(Base):
    __tablename__ = "stabling_geometry"
    stable_id = Column(String(50), primary_key=True, index=True)
    train_id = Column(String(50), index=True)
    coach_id = Column(String(50))
    length_m = Column(Integer)
    width_m = Column(Integer)
    height_m = Column(Integer)
    yard_location = Column(String(100))
