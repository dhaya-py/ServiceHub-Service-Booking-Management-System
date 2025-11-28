# app/api/routes/admin.py
from fastapi import APIRouter, Depends
from app.core.security import require_admin
from app.schemas.user import UserResponse
from app.db.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/test", response_model=dict)
def admin_test(user: User = Depends(require_admin)):
    return {"ok": True, "message": "Admin access granted", "admin": user.email}
