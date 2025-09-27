# CRUD operations package
from .trains import read_train, read_trains, create_train, update_train, delete_train
from .fitness import (read_fitness_certificate, read_fitness_certificates, 
                     create_fitness_certificate, update_fitness_certificate, 
                     delete_fitness_certificate, read_valid_certificates)
from .job_cards import (read_job_card, read_job_cards, create_job_card, 
                       update_job_card, delete_job_card, read_open_job_cards)
from .branding import (read_branding_contract, read_branding_contracts, 
                      create_branding_contract, update_branding_contract, 
                      delete_branding_contract, read_active_contracts, read_contracts_by_train)
from .cleaning import (read_cleaning_slot, read_cleaning_slots, create_cleaning_slot, 
                      update_cleaning_slot, delete_cleaning_slot)
from .stabling import (read_stabling_geometry, read_stabling_geometries, 
                      create_stabling_geometry, update_stabling_geometry, 
                      delete_stabling_geometry)
from .induction import (read_induction_plan, read_induction_plans, 
                       create_induction_plan, update_induction_plan, 
                       delete_induction_plan, read_todays_plan)
from .feedback import (read_feedback, read_all_feedback, create_feedback, 
                      update_feedback, delete_feedback)
from .performance import (get_train_performance_history, get_crew_availability,
                         get_maintenance_priority, get_branding_priority)

__all__ = [
    # Trains
    "read_train", "read_trains", "create_train", "update_train", "delete_train",
    # Fitness
    "read_fitness_certificate", "read_fitness_certificates", "create_fitness_certificate",
    "update_fitness_certificate", "delete_fitness_certificate", "read_valid_certificates",
    # Job Cards
    "read_job_card", "read_job_cards", "create_job_card", "update_job_card",
    "delete_job_card", "read_open_job_cards",
    # Branding
    "read_branding_contract", "read_branding_contracts", "create_branding_contract",
    "update_branding_contract", "delete_branding_contract", "read_active_contracts", "read_contracts_by_train",
    # Cleaning
    "read_cleaning_slot", "read_cleaning_slots", "create_cleaning_slot",
    "update_cleaning_slot", "delete_cleaning_slot",
    # Stabling
    "read_stabling_geometry", "read_stabling_geometries", "create_stabling_geometry",
    "update_stabling_geometry", "delete_stabling_geometry",
    # Induction
    "read_induction_plan", "read_induction_plans", "create_induction_plan",
    "update_induction_plan", "delete_induction_plan", "read_todays_plan",
    # Feedback
    "read_feedback", "read_all_feedback", "create_feedback", "update_feedback", "delete_feedback",
    # Performance (NEW - Add these)
    "get_train_performance_history", "get_crew_availability", 
    "get_maintenance_priority", "get_branding_priority"
]