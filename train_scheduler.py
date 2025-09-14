# train_scheduler.py

import pandas as pd
from datetime import datetime, timedelta
from data_loader import load_data

class TrainScheduler:
    def __init__(self, rakes, jobs, today):
        self.rakes = rakes
        self.jobs = jobs
        self.today = today
        self.schedule = []

    # -------------------------------
    # Rule 1: Mileage Balancing
    # -------------------------------
    def prioritize_rake_by_mileage(self, rake):
        ratio = rake.current_mileage / rake.max_mileage
        if ratio >= 0.9:
            return 0  # highest priority
        elif ratio < 0.6:
            return 2  # low priority
        else:
            return 1  # medium

    # -------------------------------
    # Rule 2: Fitness Certificate
    # -------------------------------
    def fitness_high_priority(self, rake):
        return (rake.fitness_valid_till - self.today).days < 7 or rake.fitness_status.lower() in ["fail", "restricted"]

    # -------------------------------
    # Rule 3: Compatibility
    # -------------------------------
    def is_compatible(self, job, rake):
        return job.required_rake_type == rake.rake_type

    # -------------------------------
    # Rule 4: Availability Window
    # -------------------------------
    def has_availability(self, job, rake):
        window_days = (rake.next_assigned_date - rake.available_from).total_seconds() / 86400
        return job.duration_days <= window_days

    # -------------------------------
    # Rule 5: Load Balancing
    # -------------------------------
    def sort_rakes_for_job(self, job):
        return sorted(
            self.rakes,
            key=lambda r: (
                not self.fitness_high_priority(r),
                self.prioritize_rake_by_mileage(r),
                r.available_from
            )
        )

    # -------------------------------
    # Rule 6: Workshop Capacity
    # -------------------------------
    def check_workshop_capacity(self, date):
        existing_jobs = sum(1 for s in self.schedule if s["scheduled_start"].date() == date.date())
        return existing_jobs < 5  # max 5 jobs per day

    # -------------------------------
    # Rule 7: Job Dependencies (simplified)
    # -------------------------------
    def dependencies_completed(self, job):
        return True  # placeholder

    # -------------------------------
    # Scheduler
    # -------------------------------
    def schedule_jobs(self):
        # Sort jobs by deadline & priority
        jobs_sorted = sorted(
            self.jobs,
            key=lambda j: (j.deadline or (self.today + timedelta(days=30)),
                           j.client_priority or "")
        )

        for job in jobs_sorted:
            scheduled = False
            for rake in self.sort_rakes_for_job(job):
                if (self.is_compatible(job, rake)
                        and self.has_availability(job, rake)
                        and self.check_workshop_capacity(rake.available_from)
                        and self.dependencies_completed(job)):

                    # Schedule job
                    start_time = rake.available_from
                    end_time = start_time + timedelta(hours=job.duration)
                    self.schedule.append({
                        "train_id": job.train_id,
                        "coach_id": job.coach_id,
                        "job_id": job.job_id,
                        "task": job.task,
                        "scheduled_start": start_time,
                        "scheduled_end": end_time
                    })

                    # Update rake availability
                    rake.available_from = end_time
                    scheduled = True
                    break

            if not scheduled:
                print(f"⚠️ Job {job.job_id} could not be scheduled.")

        # Save schedule
        if len(self.schedule) == 0:
            print("⚠️ No jobs scheduled!")
        else:
            schedule_df = pd.DataFrame(self.schedule)
            schedule_df.to_csv("schedule.csv", index=False)
            print(f"✅ Schedule written to schedule.csv ({len(self.schedule)} jobs)")
            return schedule_df


# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    today = datetime.now()
    rakes, jobs = load_data(today)
    print(f"Loaded {len(rakes)} rakes and {len(jobs)} jobs ✅")

    scheduler = TrainScheduler(rakes, jobs, today)
    schedule_df = scheduler.schedule_jobs()

    if schedule_df is not None:
        print(schedule_df.head(10))
