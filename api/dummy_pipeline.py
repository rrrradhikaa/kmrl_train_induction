# kmrl_train_induction/api/dummy_pipeline.py
import os
import sys
import pandas as pd
from datetime import datetime
import requests

# ---- CONFIG ----
API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000")
CSV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # project root
JOB_CARDS_CSV = os.path.join(CSV_DIR, "job_cards.csv")
# ----------------

def parse_datetime(val):
    """Parse any common date/datetime format and return DD-MM-YYYY HH:MM."""
    if pd.isna(val) or val is None:
        return None
    s = str(val).strip()
    # common formats
    fmts = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
    ]
    for f in fmts:
        try:
            dt = datetime.strptime(s, f)
            # Convert to DD-MM-YYYY HH:MM for FastAPI
            return dt.strftime("%d-%m-%Y %H:%M")
        except Exception:
            continue
    # last resort: return as string (FastAPI will likely reject if invalid)
    return s

def load_job_cards():
    if not os.path.exists(JOB_CARDS_CSV):
        print("CSV not found:", JOB_CARDS_CSV)
        sys.exit(1)

    df = pd.read_csv(JOB_CARDS_CSV)
    df = df.where(pd.notnull(df), None)
    success = 0
    errors = 0

    for idx, row in df.iterrows():
        payload = {
            "job_id": str(row.get("job_id")) if row.get("job_id") else f"JC-CSV-{idx+1}",
            "train_id": row.get("train_id"),
            "coach_id": row.get("coach_id"),
            "task": row.get("task"),
            "status": row.get("status"),
            "assigned_to": row.get("assigned_to"),
            "scheduled_date": parse_datetime(row.get("scheduled_date"))
        }

        # Remove None values so validation may accept optional fields
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            r = requests.post(f"{API_BASE}/job_cards/", json=payload, timeout=10)
            if r.status_code in (200, 201):
                success += 1
                print(f"[OK] {payload['job_id']}")
            else:
                errors += 1
                print(f"[ERR {r.status_code}] {payload['job_id']} -> {r.text}")
        except Exception as e:
            errors += 1
            print(f"[EXC] {payload['job_id']} -> {e}")

    print(f"\nDone. Success={success} Errors={errors}")

if __name__ == "__main__":
    load_job_cards()
