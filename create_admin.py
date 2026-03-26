"""
Create an admin account for ServiceHub.
Usage: python create_admin.py [email] [password] [name]

Example:
    python create_admin.py admin@servicehub.com admin123 "Super Admin"
"""
import sys
from app.db.base import SessionLocal
from app.db.models.user import User
from app.core.security import hash_password


def create_admin(email: str, password: str, name: str = "Admin"):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            if existing.role == "admin":
                print(f"Admin account '{email}' already exists.")
            else:
                # Promote existing user to admin
                existing.role = "admin"
                db.commit()
                print(f"Existing user '{email}' promoted to admin.")
            return

        admin = User(
            email=email,
            name=name,
            password_hash=hash_password(password),
            role="admin",
        )
        db.add(admin)
        db.commit()
        print(f"Admin account created: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py <email> <password> [name]")
        print('Example: python create_admin.py admin@servicehub.com admin123 "Super Admin"')
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    name = sys.argv[3] if len(sys.argv) > 3 else "Admin"

    create_admin(email, password, name)
