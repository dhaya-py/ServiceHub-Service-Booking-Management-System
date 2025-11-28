# app/api/routes/provider.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.db.models.user import User, provider_categories
from app.db.models.category import Category
from app.schemas.provider import ProviderCreate, ProviderUpdate, ProviderResponse
from app.core.security import require_admin, get_current_user
from app.core.security import hash_password

router = APIRouter(prefix="/providers", tags=["providers"])

# ADMIN: create a provider and assign categories
@router.post("/", response_model=ProviderResponse)
def admin_create_provider(
    payload: ProviderCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    # email unique
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    provider = User(
        email=payload.email,
        name=payload.name,
        password_hash=hash_password(payload.password),
        role="provider",
        phone=payload.phone,
        address=payload.address,
        description=payload.description
    )

    # attach categories if provided
    if payload.category_ids:
        categories = db.query(Category).filter(Category.id.in_(payload.category_ids)).all()
        if not categories:
            raise HTTPException(status_code=400, detail="Invalid category ids")
        provider.categories = categories

    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


# PUBLIC: list providers, optionally filter by category_id
@router.get("/", response_model=List[ProviderResponse])
def list_providers(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(User).filter(User.role == "provider")
    if category_id:
        q = q.join(provider_categories).filter(provider_categories.c.category_id == category_id)
    providers = q.all()
    return providers


# PUBLIC: get provider by id
@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(User).filter(User.id == provider_id, User.role == "provider").first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


# PROVIDER (self) or ADMIN: update profile
@router.put("/me", response_model=ProviderResponse)
def update_own_profile(
    payload: ProviderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "provider" and current_user.role != "admin":
        # admin can update any provider using a different endpoint later
        raise HTTPException(status_code=403, detail="Provider access only")

    # allow providers to update own profile
    user = db.query(User).filter(User.id == current_user.id).first()
    if payload.name is not None:
        user.name = payload.name
    if payload.phone is not None:
        user.phone = payload.phone
    if payload.address is not None:
        user.address = payload.address
    if payload.description is not None:
        user.description = payload.description
    if payload.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(payload.category_ids)).all()
        user.categories = categories

    db.commit()
    db.refresh(user)
    return user


# ADMIN: assign categories to an existing provider
@router.post("/{provider_id}/categories", response_model=ProviderResponse)
def admin_assign_categories(provider_id: int, category_ids: List[int], db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    provider = db.query(User).filter(User.id == provider_id, User.role == "provider").first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    categories = db.query(Category).filter(Category.id.in_(category_ids)).all()
    if not categories:
        raise HTTPException(status_code=400, detail="Invalid category ids")

    # add (avoids duplicates because relationship is set)
    for c in categories:
        if c not in provider.categories:
            provider.categories.append(c)

    db.commit()
    db.refresh(provider)
    return provider


# ADMIN: remove category from provider
@router.delete("/{provider_id}/categories/{category_id}", response_model=ProviderResponse)
def admin_remove_category(provider_id: int, category_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    provider = db.query(User).filter(User.id == provider_id, User.role == "provider").first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    category = db.query(Category).filter(Category.id == category_id).first()
    if category in provider.categories:
        provider.categories.remove(category)
        db.commit()
        db.refresh(provider)

    return provider
