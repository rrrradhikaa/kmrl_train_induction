# 🚆 Train Scheduling Algorithm - Draft (M4)

## ✅ Task: Draft scheduling rules (pseudo-code)

This document contains the initial logic and business rules for scheduling train maintenance job cards, with focus on:

- Mileage balancing
- Fitness certificate tracking
- Availability windows
- Job compatibility

---

## ⚙️ Rule 1: Mileage Balancing

```pseudo
For each rake in the system:
    If mileage >= 90% of max allowed mileage:
        Prioritize this rake for upcoming job cards
Rule 2: Fitness Certificate Expiry
For each rake:
    If fitness_certificate.expiry_date < (today + 7 days):
        Flag as HIGH PRIORITY for scheduling
Purpose: Avoid running trains with expiring fitness certificates.
Rule 3: Job Compatibility Check
For each job_card:
    Check required_rake_type (e.g., LHB, ICF)
    Filter only those rakes that match the required type and are currently available
Purpose: Only assign jobs to compatible rakes.
Rule 4: Availability Window
For each rake:
    Check available_from and next_assigned_date
    If job duration fits within this window:
        Mark as AVAILABLE for scheduling
Purpose: Avoid overlapping or tight maintenance windows.
Rule 5: Load Balancing
Sort rakes by (current_mileage / max_mileage)
Distribute jobs to keep mileage usage balanced across fleet
Purpose: Ensure fair and efficient usage of all rakes.
