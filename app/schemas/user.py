# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    class Config:
        # allow returning SQLAlchemy objects directly
        from_attributes = True

# Optional: schema for admin creation if you want admin to create users with roles
class AdminCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str
