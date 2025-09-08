# 🚆 Train Scheduling Algorithm - Draft (M4)

## ✅ Task: Draft scheduling rules (pseudo-code)

This document contains the initial logic and business rules for scheduling train maintenance job cards, with a focus on:

- ✅ Mileage Balancing  
- ✅ Fitness Certificate Tracking  
- ✅ Availability Windows  
- ✅ Job Compatibility  
- ✅ Load Distribution  
- ✅ Workshop Capacity Handling  
- ✅ Job Dependency Resolution

---

## ⚙️ Rule 1: Mileage Balancing

```pseudo
For each rake in the system:
    If mileage >= 90% of max allowed mileage:
        Prioritize this rake for upcoming job cards
    Else if mileage < 60%:
        Consider deferring unless other constraints demand scheduling
Purpose: Prevent overuse of a few rakes and spread maintenance load across the fleet.


📅 Rule 2: Fitness Certificate Expiry
For each rake:
    If fitness_certificate.expiry_date < (today + 7 days):
        Flag as HIGH PRIORITY for scheduling
Purpose: Avoid running trains with expiring fitness certificates.


🔧 Rule 3: Job Compatibility Check
For each job_card:
    Check required_rake_type (e.g., LHB, ICF)
    Filter only those rakes that match the required type and are currently available
Purpose: Only assign jobs to compatible rake types to avoid mismatches.


⏳ Rule 4: Availability Window
For each rake:
    Check (available_from, next_assigned_date)
    Calculate available_maintenance_window = next_assigned_date - available_from

    If job_card.duration <= available_maintenance_window:
        Mark as AVAILABLE for scheduling
Purpose: Ensure the job fits within the window when the rake is not in active service.


⚖️ Rule 5: Load Balancing
Sort rakes by (current_mileage / max_mileage)
Assign priority in a rotating manner to ensure:
    - Equal opportunity for low-usage and high-usage rakes
    - Even distribution of job cards over the fleet
Purpose: Prevent scenarios where a few rakes are always scheduled while others are idle.


🏭 Rule 6: Workshop Capacity Constraints
For each date:
    Check workshop_capacity[date]
    If capacity_remaining > 0:
        Schedule job
    Else:
        Push to next available date
Purpose: Avoid exceeding physical capacity of the maintenance facility.


🔗 Rule 7: Job Dependency Resolution
For each rake:
    For each job_card:
        If job_card has dependencies (e.g., FC before IOH):
            Ensure dependency is already completed or scheduled before this job
Purpose: Maintain logical correctness in job execution order.
