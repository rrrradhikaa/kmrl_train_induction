import os
import logging
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from kmrl_train_induction.mock_api.database import engine, SessionLocal, Base
from kmrl_train_induction.mock_api import models

# --------------------------
# Setup Logging
# --------------------------
LOG_FILE = os.path.join(os.path.dirname(__file__), "load_csv.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")  # Log file
    ]
)

# --------------------------
# Create Tables if Not Exist
# --------------------------
Base.metadata.create_all(bind=engine)

def load_csv_to_db():
    db: Session = SessionLocal()

    csv_mapping = {
        "fitness_certificates.csv": models.FitnessCertificate,
        "job_cards.csv": models.JobCard,
        "branding_priorities.csv": models.BrandingPriority,
        "mileage_balancing.csv": models.MileageBalancing,
        "cleaning_slots.csv": models.CleaningSlot,
        "stabling_geometry.csv": models.StablingGeometry
    }

    for csv_file, model in csv_mapping.items():
        file_path = os.path.join(os.path.dirname(__file__), "..", csv_file)
        abs_path = os.path.abspath(file_path)
        logging.info(f"📂 Loading file: {abs_path}")

        if not os.path.exists(abs_path):
            logging.error(f"❌ File not found: {abs_path}")
            continue

        try:
            # Truncate table safely using `text()`
            logging.info(f"🗑️ Truncating table `{model.__tablename__}`...")
            db.execute(text(f"TRUNCATE TABLE {model.__tablename__} RESTART IDENTITY CASCADE;"))
            db.commit()

            # Read CSV
            df = pd.read_csv(abs_path)
            df = df.where(pd.notnull(df), None)

            # Insert data
            db.bulk_insert_mappings(model, df.to_dict(orient="records"))
            db.commit()

            logging.info(f"✅ Loaded {len(df)} records into `{model.__tablename__}`")

        except Exception as e:
            db.rollback()
            logging.error(f"❌ Failed to load `{csv_file}`: {e}")

    db.close()
    logging.info("🎉 All CSV data loaded successfully.")

if __name__ == "__main__":
    load_csv_to_db()
