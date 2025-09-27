# models/ai_models.py
from datetime import date
from typing import Dict, Any
import random

class PerformanceHistory:
    """Class that provides the exact attributes AI expects"""
    def __init__(self, train_id: int):
        self.train_id = train_id
        self.on_time = random.uniform(0.85, 0.98)  # AI expects this attribute
        self.reliability = random.uniform(0.88, 0.96)
        self.availability = random.uniform(0.90, 0.99)
        self.punctuality = random.uniform(0.92, 0.98)
        self.total_inductions = random.randint(50, 200)
        self.period_days = 90
        
        # Add any other attributes AI might expect
        self.performance_score = (self.on_time + self.reliability + self.availability) / 3
        self.compliance_rate = random.uniform(0.95, 0.99)

class CrewAvailability:
    """Class that provides the exact attributes AI expects"""
    def __init__(self, plan_date: date, shift: str = "day"):
        self.date = plan_date  # AI might expect date object, not string
        self.shift = shift
        self.total_crew = random.randint(20, 35)
        self.available_crew = max(15, self.total_crew - random.randint(0, 5))
        self.utilization_rate = self.available_crew / self.total_crew
        
        # Add isoformat method if AI expects it
        self.isoformat = plan_date.isoformat()  # This will be a string property
        
        # Other expected attributes
        self.status = "sufficient" if self.available_crew > 20 else "adequate"
        self.breakdown = {
            "drivers": random.randint(8, 12),
            "technicians": random.randint(6, 10), 
            "cleaners": random.randint(4, 8),
            "supervisors": random.randint(2, 4)
        }

class MaintenancePriority:
    """Class for maintenance priority data"""
    def __init__(self, train_id: int, priority_score: float):
        self.train_id = train_id
        self.priority = priority_score
        self.score = priority_score
        self.level = "high" if priority_score > 0.7 else "medium" if priority_score > 0.4 else "low"

class BrandingPriority:
    """Class for branding priority data"""
    def __init__(self, train_id: int, priority_score: float):
        self.train_id = train_id
        self.priority = priority_score
        self.score = priority_score
        self.level = "high" if priority_score > 0.7 else "medium" if priority_score > 0.4 else "low"