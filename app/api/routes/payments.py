from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.db.base import get_db
from app.db.models.payment import Payment
from app.core.security import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/admin")
def admin_get_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
        
    payments = db.query(Payment).options(
        joinedload(Payment.customer),
        joinedload(Payment.provider),
        joinedload(Payment.booking)
    ).order_by(Payment.created_at.desc()).all()
    
    total_revenue = sum(p.amount for p in payments if p.status == "completed")
    
    results = []
    for p in payments:
        results.append({
            "id": p.id,
            "booking_id": p.booking_id,
            "amount": p.amount,
            "status": p.status,
            "transaction_id": p.transaction_id,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "customer_name": p.customer.name if p.customer else None,
            "provider_name": p.provider.name if p.provider else None
        })
        
    return {"total_revenue": total_revenue, "payments": results}

@router.get("/provider/me")
def provider_get_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Provider only")
        
    payments = db.query(Payment).options(
        joinedload(Payment.customer),
        joinedload(Payment.booking)
    ).filter(Payment.provider_id == current_user.id).order_by(Payment.created_at.desc()).all()
    
    total_earnings = sum(p.amount for p in payments if p.status == "completed")
    
    results = []
    for p in payments:
        results.append({
            "id": p.id,
            "booking_id": p.booking_id,
            "amount": p.amount,
            "status": p.status,
            "transaction_id": p.transaction_id,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "customer_name": p.customer.name if p.customer else None
        })
        
    return {"total_earnings": total_earnings, "payments": results}
