# api/backup_json.py
import os, json, psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:radhikasharma@localhost:5432/kmrl_db"
out_dir = os.path.join(os.path.dirname(__file__), "..", "backups")
os.makedirs(out_dir, exist_ok=True)

conn = psycopg2.connect(DATABASE_URL)
tables = ["fitness_certificates","job_cards","branding_priorities","mileage_balancing","cleaning_slots","stabling_geometry"]
for t in tables:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"SELECT * FROM {t};")
        rows = cur.fetchall()
    path = os.path.join(out_dir, f"{t}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, default=str, indent=2)
    print("Wrote", path)
conn.close()
