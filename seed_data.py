import csv
from database import engine, Base, SessionLocal
from models import Train, Alert

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_trains(session):
    with open("trains.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            train = Train(
                id=int(row["id"]),
                name=row["name"],
                status=row["status"],
                next_slot=row["next_slot"],
                assigned_driver=row["assigned_driver"],
                ai_confidence=float(row["ai_confidence"]),
            )
            session.merge(train)  # merge = insert or update

def seed_alerts(session):
    with open("alerts.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            alert = Alert(
                id=int(row["id"]),
                train_id=int(row["train_id"]),
                message=row["message"],
                severity=row["severity"],
            )
            session.merge(alert)

def main():
    session = SessionLocal()
    seed_trains(session)
    seed_alerts(session)
    session.commit()
    session.close()
    print("✅ Database seeded with trains & alerts!")

if __name__ == "__main__":
    main()

