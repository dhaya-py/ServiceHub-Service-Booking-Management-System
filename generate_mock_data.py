import os
import sys
from datetime import datetime, timedelta, timezone

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal, Base, engine
from app.db.models.user import User
from app.db.models.category import Category
from app.db.models.service import Service
from app.db.models.booking import Booking
from app.core.security import hash_password

IST = timezone(timedelta(hours=5, minutes=30))

def create_mock_data():
    db = SessionLocal()
    try:
        # Create tables if not exist
        # Base.metadata.create_all(bind=engine)
        
        # Check if data already exists to prevent duplicate insertion
        if db.query(User).first():
            print("Data already exists in the database. Please drop tables or delete data first if you want a fresh start.")
            # For testing, we will just proceed or we could clear it here, but let's be safe.
            print("Cleaning up existing data...")
            db.query(Booking).delete()
            db.query(Service).delete()
            db.query(Category).delete()
            db.query(User).delete()
            db.commit()

        print("Generating mock data...")

        # 1. Categories
        cat_plumbing = Category(name="Plumbing", description="Plumbing services including repair and installation")
        cat_electrical = Category(name="Electrical", description="Electrical repairs, wiring, and installations")
        cat_cleaning = Category(name="Cleaning", description="Home and office cleaning services")
        cat_carpentry = Category(name="Carpentry", description="Furniture repair, assembly, and custom woodwork")
        
        categories = [cat_plumbing, cat_electrical, cat_cleaning, cat_carpentry]
        db.add_all(categories)
        db.commit()
        for c in categories:
            db.refresh(c)
            
        print("Created Categories.")

        # 2. Users (Admin, Customers, Providers)
        password_hash = hash_password("password123")
        
        admin = User(
            email="admin@test.com",
            name="Admin User",
            password_hash=password_hash,
            role="admin",
            is_active=True
        )
        
        customer1 = User(email="customer1@test.com", name="Alice Customer", password_hash=password_hash, role="customer", phone="1234567890", address="123 Apple St")
        customer2 = User(email="customer2@test.com", name="Bob Customer", password_hash=password_hash, role="customer")
        customer3 = User(email="customer3@test.com", name="Charlie Customer", password_hash=password_hash, role="customer")

        provider1 = User(
            email="provider1@test.com", 
            name="David Provider (Plumber)", 
            password_hash=password_hash, 
            role="provider", 
            phone="9876543210", 
            is_provider_approved=True,
            is_active=True,
            categories=[cat_plumbing, cat_cleaning]
        )
        provider2 = User(
            email="provider2@test.com", 
            name="Eve Provider (Electrician)", 
            password_hash=password_hash, 
            role="provider",
            is_provider_approved=True,
            is_active=True,
            categories=[cat_electrical]
        )
        provider3 = User(
            email="provider3@test.com", 
            name="Frank Provider (Carpenter)", 
            password_hash=password_hash, 
            role="provider",
            is_provider_approved=True,
            is_active=True,
            categories=[cat_carpentry]
        )
        
        users = [admin, customer1, customer2, customer3, provider1, provider2, provider3]
        db.add_all(users)
        db.commit()
        for u in users:
            db.refresh(u)
            
        print("Created Admin, Customers, and Providers.")

        # 3. Services
        srv_plumbing_fix = Service(
            provider_id=provider1.id,
            category_id=cat_plumbing.id,
            name="Pipe Leak Repair",
            description="Fixing leaking pipes quickly and efficiently.",
            price=50.0,
            duration_minutes=60,
            is_active=True
        )
        srv_deep_clean = Service(
            provider_id=provider1.id,
            category_id=cat_cleaning.id,
            name="House Deep Cleaning",
            description="Thorough deep cleaning of all rooms.",
            price=150.0,
            duration_minutes=180,
            is_active=True
        )
        srv_wiring = Service(
            provider_id=provider2.id,
            category_id=cat_electrical.id,
            name="Electrical Wiring Repair",
            description="Safe and secure electrical wiring fixes.",
            price=80.0,
            duration_minutes=120,
            is_active=True
        )
        srv_furniture = Service(
            provider_id=provider3.id,
            category_id=cat_carpentry.id,
            name="Furniture Assembly",
            description="Assembling IKEA or other furniture.",
            price=40.0,
            duration_minutes=60,
            is_active=True
        )
        
        services = [srv_plumbing_fix, srv_deep_clean, srv_wiring, srv_furniture]
        db.add_all(services)
        db.commit()
        for s in services:
            db.refresh(s)
            
        print("Created Services.")

        # 4. Bookings
        now = datetime.now(IST)
        
        b1 = Booking(
            customer_id=customer1.id,
            provider_id=provider1.id,
            service_id=srv_plumbing_fix.id,
            booking_date=(now + timedelta(days=1)).date(),
            booking_time=(now + timedelta(hours=2)).time(),
            amount=srv_plumbing_fix.price,
            status="pending",
            address="123 Apple St"
        )
        
        b2 = Booking(
            customer_id=customer2.id,
            provider_id=provider2.id,
            service_id=srv_wiring.id,
            booking_date=(now + timedelta(days=2)).date(),
            booking_time=(now + timedelta(hours=1)).time(),
            amount=srv_wiring.price,
            status="confirmed",
            address="456 Banana Rd"
        )
        
        b3 = Booking(
            customer_id=customer3.id,
            provider_id=provider3.id,
            service_id=srv_furniture.id,
            booking_date=(now - timedelta(days=1)).date(),
            booking_time=(now).time(),
            amount=srv_furniture.price,
            status="completed",
            address="789 Cherry Blvd"
        )
        
        bookings = [b1, b2, b3]
        db.add_all(bookings)
        db.commit()
        
        print("Created Bookings.")
        print("-" * 30)
        print("Mock Data Generation Complete!")
        print("Test Accounts:")
        print("Admin: admin@test.com / password123")
        print("Customer: customer1@test.com / password123")
        print("Provider (Plumber): provider1@test.com / password123")

    except Exception as e:
        print(f"Error generating data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_mock_data()
