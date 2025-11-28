# app/schemas/provider.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.schemas.category import CategoryMiniResponse


class ProviderCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    category_ids: Optional[List[int]] = []

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    category_ids: Optional[List[int]] = None

class ProviderResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    categories: List[CategoryMiniResponse] = []  # will return minimal category objects

    class Config:
        from_attributes = True
