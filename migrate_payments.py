import sqlite3
import os
from sqlalchemy import create_engine
from app.db.base import Base

# Must import all models to ensure they register to Base
from app.db.models.user import User
from app.db.models.service import Service
from app.db.models.category import Category
from app.db.models.booking import Booking
from app.db.models.availability import ProviderAvailability
from app.db.models.review import Review
from app.db.models.notification import Notification
from app.db.models.payment import Payment

db_path = "d:/personal-projects/service-booking-platform/service-booking-platform/servicehub.db"

# 1. Raw SQLite to Alter bookings table safely
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("Checking if payment_status exists in bookings...")
    cursor.execute("PRAGMA table_info(bookings)")
    columns = [info[1] for info in cursor.fetchall()]
    if "payment_status" not in columns:
        print("Adding payment_status column to bookings...")
        cursor.execute("ALTER TABLE bookings ADD COLUMN payment_status VARCHAR DEFAULT 'paid'")
        conn.commit()
    else:
        print("payment_status already exists in bookings.")
    
    conn.close()
except Exception as e:
    print("Migration alter error:", e)

# 2. SQLAlchemy create_all to natively generate the NEW payments table without dropping anything
SQLALCHEMY_DATABASE_URL = "sqlite:///./servicehub.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

print("Creating native tables for newly registered models (Payment)...")
Base.metadata.create_all(bind=engine)
print("Migration completed safely!")
