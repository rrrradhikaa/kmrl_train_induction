import os
import pandas as pd
from sqlalchemy.orm import Session
from mock_api.database import engine, SessionLocal, Base
from mock_api import models

# Tables create karna
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
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", csv_file))
        print(f"Loading file: {csv_path}")

        if not os.path.exists(csv_path):
            print(f"❌ Error: {csv_file} not found at path {csv_path}")
            continue

        df = pd.read_csv(csv_path)
        df = df.fillna(None)

        for _, row in df.iterrows():
            record = model(**row.to_dict())
            db.add(record)

        db.commit()
        print(f"✅ {csv_file} loaded successfully.")

    db.close()
    print("🎉 All CSV data loaded successfully.")

if __name__ == "__main__":
    load_csv_to_db()
