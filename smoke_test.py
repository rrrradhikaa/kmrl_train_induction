# api/smoke_test.py
import os, requests, json, sys
BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

def call(path, method="GET", payload=None):
    url = BASE + path
    print("->", method, url)
    r = requests.request(method, url, json=payload, timeout=8)
    print(r.status_code)
    try:
        print(r.json())
    except Exception:
        print(r.text[:200])
    print("-"*40)
    return r

def main():
    # health
    call("/")
    # list
    call("/fitness_certificates/")
    # create a demo record (certificate_id is PK and must be provided)
    demo = {
      "certificate_id": "DEMO-FC-20250909",
      "train_id":"T999",
      "coach_id":"C999",
      "fitness_check_date":"09-09-2025",
      "fitness_status":"Pass",
      "issued_by":"DemoInspector",
      "valid_till":"3-09-2025",
      "odometer_km":1000,
      "remarks":"smoke-test"
    }
    r = call("/fitness_certificates/", "POST", demo)
    if r.status_code in (200,201):
        call("/fitness_certificates/DEMO-FC-20250909")
    # cleanup
    call("/fitness_certificates/DEMO-FC-20250909", "DELETE")
    print("SMOKE DONE")

if __name__ == "__main__":
    main()
