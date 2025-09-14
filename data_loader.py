# data_loader.py

import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class Rake:
    train_id: str
    coach_id: str
    current_mileage: int
    max_mileage: int
    fitness_valid_till: datetime
    fitness_status: str
    rake_type: str
    available_from: datetime
    next_assigned_date: datetime

@dataclass
class JobCard:
    train_id: str
    coach_id: str
    job_id: str
    task: str
    required_rake_type: str
    duration: int  # hours
    scheduled_date: datetime
    dependencies: List[str]
    deadline: datetime = None
    client_priority: str = None

    @property
    def duration_days(self):
        return self.duration / 24  # convert hours to fractional days

def load_data(today: datetime):
    # Load CSVs
    fitness_df = pd.read_csv("fitness_certificates.csv")
    fitness_df.columns = fitness_df.columns.str.strip()

    job_df = pd.read_csv("job_cards.csv")
    job_df.columns = job_df.columns.str.strip()

    branding_df = pd.read_csv("branding_priorities.csv")
    branding_df.columns = branding_df.columns.str.strip()

    mileage_df = pd.read_csv("mileage_balancing.csv")
    mileage_df.columns = mileage_df.columns.str.strip()

    stabling_df = pd.read_csv("stabling_geometry.csv")
    stabling_df.columns = stabling_df.columns.str.strip()

    cleaning_df = pd.read_csv("cleaning_slots.csv")
    cleaning_df.columns = cleaning_df.columns.str.strip()

    # Build rakes
    rakes = []
    for _, row in mileage_df.iterrows():
        fitness_row = fitness_df[fitness_df["coach_id"] == row["coach_id"]].iloc[0]

        rake = Rake(
            train_id=row["train_id"],
            coach_id=row["coach_id"],
            current_mileage=int(row["odometer_km"]),
            max_mileage=int(row["next_due_km"]),
            fitness_valid_till=datetime.strptime(str(fitness_row["valid_till"]), "%d-%m-%Y"),
            fitness_status=str(fitness_row["fitness_status"]),
            rake_type="LHB",  # placeholder, can extend later
            available_from=today,
            next_assigned_date=today + pd.Timedelta(days=1),  # one-day availability window
        )
        rakes.append(rake)

    # Build jobs
    jobs = []
    for _, row in job_df.iterrows():
        bp_row = branding_df[(branding_df["train_id"] == row["train_id"]) &
                             (branding_df["coach_id"] == row["coach_id"])]
        deadline = None
        priority = None
        if not bp_row.empty:
            deadline = datetime.strptime(str(bp_row["deadline"].values[0]).split(" ")[0], "%Y-%m-%d")
            priority = bp_row["priority"].values[0]

        job = JobCard(
            train_id=row["train_id"],
            coach_id=row["coach_id"],
            job_id=row["job_id"],
            task=row["task"],
            required_rake_type="LHB",
            duration=4,  # placeholder in hours
            scheduled_date=datetime.strptime(str(row["scheduled_date"]).split(" ")[0], "%Y-%m-%d"),
            dependencies=[],
            deadline=deadline,
            client_priority=priority,
        )
        jobs.append(job)

    return rakes, jobs

if __name__ == "__main__":
    today = datetime.now()
    rakes, jobs = load_data(today)
    print(f"Loaded {len(rakes)} rakes and {len(jobs)} jobs ✅")
