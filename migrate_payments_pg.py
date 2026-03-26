from app.db.base import engine, Base
from sqlalchemy import text
from app.db.models.payment import Payment
from app.db.models.user import User
from app.db.models.service import Service
from app.db.models.category import Category
from app.db.models.booking import Booking
from app.db.models.availability import ProviderAvailability
from app.db.models.review import Review
from app.db.models.notification import Notification
import sys

# Raw SQLAlchemy to alter bookings safely in PostgreSQL
try:
    with engine.begin() as conn:
        print("Checking tables in PostgreSQL...")
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bookings'")).fetchall()
        columns = [row[0] for row in result]
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
