from app.db.base import engine, Base
from sqlalchemy import text
from app.db.models.payment import Payment
import sys

# Raw SQLAlchemy to alter bookings safely
try:
    with engine.begin() as conn:
        print("Checking tables...")
        result = conn.execute(text("PRAGMA table_info(bookings);")).fetchall()
        columns = [row[1] for row in result]
        if "payment_status" not in columns:
            print("Adding payment_status column...")
            conn.execute(text("ALTER TABLE bookings ADD COLUMN payment_status VARCHAR DEFAULT 'pending'"))
        else:
            print("payment_status exists.")
            
        print("Creating Base Metadata models...")
        Base.metadata.create_all(bind=engine)
        print("Success.")
except Exception as e:
    print("Error:", e)
