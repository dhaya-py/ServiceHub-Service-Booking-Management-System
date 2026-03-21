from app.db.base import SessionLocal
from app.db.models.availability import ProviderAvailability
db = SessionLocal()
avails = db.query(ProviderAvailability).all()
print(f"Total avails: {len(avails)}")
if len(avails) > 0:
    for a in avails[:10]:
        print(f"Provider: {a.provider_id}, Day: {a.weekday}, time: {a.start_time}-{a.end_time}, active: {a.is_active}")
