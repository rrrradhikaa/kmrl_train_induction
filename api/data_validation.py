# kmrl_train_induction/api/data_validation.py
import os, sys
import pandas as pd
from dateutil import parser
from typing import List

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FILES = {
    "fitness_certificates.csv": ["train_id","coach_id","fitness_check_date","fitness_status","defects_found","certificate_id","issued_by","valid_till","odometer_km","remarks"],
    "job_cards.csv": ["train_id","coach_id","job_id","task","status","assigned_to","scheduled_date"],
    "branding_priorities.csv": ["train_id","coach_id","brand_task","priority","deadline","owner_team"],
    "mileage_balancing.csv": ["train_id","coach_id","odometer_km","balance_action","next_due_km","remarks"],
    "cleaning_slots.csv": ["train_id","coach_id","slot_id","location","cleaning_time","cleaning_type","assigned_cleaner"],
    "stabling_geometry.csv": ["train_id","coach_id","stable_id","length_m","width_m","height_m","yard_location"]
}

def try_parse_date(s):
    if pd.isna(s) or s is None: return None
    try:
        dt = parser.parse(str(s), dayfirst=True)  # Accept DD-MM-YYYY and YYYY-MM-DD
        return dt.date().isoformat()
    except Exception:
        return None

def validate_csv(path, required_cols: List[str]):
    print(f"--- Validating {os.path.basename(path)} ---")
    df = pd.read_csv(path, dtype=str)
    # columns check
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        print("MISSING COLUMNS:", missing_cols)
    else:
        print("All required columns present")
    # missing values count
    na_counts = df[required_cols].isna().sum()
    print("Missing counts (per required column):")
    print(na_counts[na_counts>0].to_dict())
    # date checks: try parse known date fields
    for col in ["fitness_check_date","valid_till","scheduled_date","deadline","cleaning_time"]:
        if col in df.columns:
            bad = 0
            for v in df[col].tolist():
                if v is None or (isinstance(v, float) and pd.isna(v)): 
                    continue
                if try_parse_date(v) is None:
                    bad += 1
            print(f"Column {col}: bad dates = {bad}")
    print("Row count:", len(df))
    return df

def main():
    overall_ok = True
    for fn, cols in CSV_FILES.items():
        path = os.path.join(ROOT, fn)
        if not os.path.exists(path):
            print("File missing:", path)
            overall_ok = False
            continue
        validate_csv(path, cols)
    if overall_ok:
        print("\nValidation complete: CSV files present. Fix reported issues before ingestion.")
    else:
        print("\nValidation incomplete: Missing files.")

if __name__ == "__main__":
    main()
