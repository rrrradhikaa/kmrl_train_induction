import random

# Rule 1: Job Prioritization
def categorize_priority(deadline, client):
    if deadline < 24 or client == "Premium":
        return "High"
    elif 24 <= deadline <= 72:
        return "Medium"
    else:
        return "Low"

# Rule 2: Time Slot Mapping
def categorize_time_slot(hour):
    if 0 <= hour < 6:
        return "Batch Window"
    elif 6 <= hour < 10:
        return "API Priority"
    elif 10 <= hour < 18:
        return "Client Jobs"
    else:
        return "Deferred/Monitoring"

# Rule 3: Resource Simulation
def simulate_resources():
    return {
        'CPU': random.randint(40, 95),
        'Memory': random.randint(30, 85),
        'DB': random.randint(25, 95)
    }

# Rule 4: Retry Logic
def apply_retry_logic(job_type, resources):
    if job_type == "BackgroundSync" and resources['CPU'] > 90:
        return "Deferred due to high CPU"
    if job_type == "Batch":
        for i, delay in enumerate([1, 2, 4]):
            # Simulate success/failure (80% chance of success on retry)
            if random.random() < 0.8:
                return f"Completed on Retry {i+1} after {delay}s"
        return "Failed after retries"
    if job_type == "API":
        for i, delay in enumerate([2, 5]):
            if random.random() < 0.9:
                return f"API Success on Retry {i+1}"
        return "API Timeout – Logged & Notified"
    return "Executed"
