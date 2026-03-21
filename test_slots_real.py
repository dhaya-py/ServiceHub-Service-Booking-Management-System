from app.db.base import SessionLocal
from app.db.models.service import Service
from app.db.models.user import User
import requests

db = SessionLocal()
service = db.query(Service).filter(Service.name == "House Deep Cleaning").first()
if service:
    print("Found service:", service.id, "duration:", service.duration_minutes)
    r2 = requests.get(f"http://127.0.0.1:8000/availability/provider/{service.provider_id}/slots?service_id={service.id}&date_str=2026-03-20")
    print("Slots 200?:", r2.status_code)
    slots = r2.json()
    print("Slots returned:", len(slots))
    for s in slots:
        print("-", s)
else:
    print("Service not found")
