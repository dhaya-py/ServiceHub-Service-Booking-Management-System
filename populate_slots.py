from app.db.base import SessionLocal
from app.db.models.user import User
from app.db.models.availability import ProviderAvailability
from datetime import time

def add_slots():
    db = SessionLocal()
    try:
        providers = db.query(User).filter(User.role == "provider").all()
        for p in providers:
            # clear existing
            db.query(ProviderAvailability).filter(ProviderAvailability.provider_id == p.id).delete()
            for i in range(1, 8):
                db.add(ProviderAvailability(
                    provider_id=p.id,
                    weekday=i,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                    is_active=True
                ))
        db.commit()
        print("Done populating slots for properties")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_slots()
