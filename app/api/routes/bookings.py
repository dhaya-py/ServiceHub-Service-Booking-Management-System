from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from app.db.base import get_db
from app.db.models.booking import Booking
from app.db.models.service import Service
from app.db.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.core.security import get_current_user

from datetime import datetime, timedelta
from app.db.models.availability import ProviderAvailability, ProviderTimeOff
from app.api.routes.availability import is_blocked_by_timeoff, overlaps, get_provider_bookings_on_date

router = APIRouter(prefix="/bookings", tags=["bookings"])


def _load_booking_with_relations(db: Session, booking_id: int):
    """Load a booking with its relationships eagerly loaded."""
    return db.query(Booking).options(
        joinedload(Booking.service),
        joinedload(Booking.provider),
        joinedload(Booking.customer)
    ).filter(Booking.id == booking_id).first()


def _booking_to_response(booking) -> dict:
    """Convert a booking ORM object to a response dict with names."""
    return BookingResponse.from_orm_with_names(booking)


def _load_bookings_with_relations(db: Session, query):
    """Load bookings with eager loading of relationships."""
    return query.options(
        joinedload(Booking.service),
        joinedload(Booking.provider),
        joinedload(Booking.customer)
    ).all()


# Customer creates booking
@router.post("/customer")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can create bookings")

    service = db.query(Service).filter(Service.id == booking.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(User).filter(
        User.id == booking.provider_id, User.role == "provider"
    ).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    weekday = booking.booking_date.weekday() + 1
    requested_start = datetime.combine(booking.booking_date, booking.booking_time)
    requested_end = requested_start + timedelta(minutes=service.duration_minutes)

    avail_windows = db.query(ProviderAvailability).filter(
        ProviderAvailability.provider_id == booking.provider_id,
        ProviderAvailability.weekday == weekday,
        ProviderAvailability.is_active == True
    ).all()
    if not avail_windows:
        raise HTTPException(status_code=400, detail="Provider has no availability on this day")

    ok_window = False
    for w in avail_windows:
        window_start = datetime.combine(booking.booking_date, w.start_time)
        window_end = datetime.combine(booking.booking_date, w.end_time)
        if requested_start >= window_start and requested_end <= window_end:
            ok_window = True
            break
    if not ok_window:
        raise HTTPException(status_code=400, detail="Requested time is outside provider availability")

    existing = get_provider_bookings_on_date(db, booking.provider_id, booking.booking_date)
    for b_start, b_end in existing:
        if overlaps(b_start, b_end, requested_start, requested_end):
            raise HTTPException(status_code=400, detail="Requested time overlaps an existing booking")

    if is_blocked_by_timeoff(db, booking.provider_id, requested_start, requested_end):
        raise HTTPException(status_code=400, detail="Requested time falls during provider time off")

    new_booking = Booking(
        customer_id=current_user.id,
        provider_id=booking.provider_id,
        service_id=booking.service_id,
        booking_date=booking.booking_date,
        booking_time=booking.booking_time,
        address=booking.address,
        amount=booking.amount,
        status="pending",
        payment_status="paid"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    import uuid
    from app.db.models.payment import Payment
    tx_id = f"tx_{uuid.uuid4().hex[:10]}"
    new_payment = Payment(
        booking_id=new_booking.id,
        customer_id=current_user.id,
        provider_id=booking.provider_id,
        amount=booking.amount,
        status="completed",
        transaction_id=tx_id
    )
    db.add(new_payment)
    db.commit()

    loaded = _load_booking_with_relations(db, new_booking.id)
    return _booking_to_response(loaded)


# Customer cancels booking
@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Customers only")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    if booking.status != "pending":
        raise HTTPException(status_code=400, detail=f"Cannot cancel booking because it is already {booking.status}")

    booking.status = "canceled"
    db.commit()
    db.refresh(booking)

    loaded = _load_booking_with_relations(db, booking.id)
    return _booking_to_response(loaded)


# Customer views their bookings
@router.get("/customer/me")
def customer_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Customers only")

    bookings = _load_bookings_with_relations(
        db,
        db.query(Booking).filter(Booking.customer_id == current_user.id).order_by(Booking.created_at.desc())
    )
    return [_booking_to_response(b) for b in bookings]


# Provider views their bookings
@router.get("/provider/me")
def provider_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Only providers can view this")

    bookings = _load_bookings_with_relations(
        db,
        db.query(Booking).filter(Booking.provider_id == current_user.id).order_by(Booking.created_at.desc())
    )
    return [_booking_to_response(b) for b in bookings]


# Provider accepts booking
@router.post("/{booking_id}/accept")
def accept_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Providers only")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    if booking.status != "pending":
        raise HTTPException(status_code=400, detail="Booking already handled")

    booking.status = "accepted"
    db.commit()
    db.refresh(booking)

    loaded = _load_booking_with_relations(db, booking.id)
    return _booking_to_response(loaded)


# Provider rejects booking
@router.post("/{booking_id}/reject")
def reject_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Providers only")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    if booking.status != "pending":
        raise HTTPException(status_code=400, detail="Booking already handled")

    booking.status = "rejected"
    db.commit()
    db.refresh(booking)

    loaded = _load_booking_with_relations(db, booking.id)
    return _booking_to_response(loaded)


# Provider completes booking
@router.post("/{booking_id}/complete")
def complete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Providers only")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    if booking.status != "accepted":
        raise HTTPException(status_code=400, detail="Only accepted bookings can be completed")

    booking.status = "completed"
    db.commit()
    db.refresh(booking)

    loaded = _load_booking_with_relations(db, booking.id)
    return _booking_to_response(loaded)


# Admin views all bookings
@router.get("/admin/all")
def admin_all_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    bookings = _load_bookings_with_relations(
        db,
        db.query(Booking).order_by(Booking.created_at.desc())
    )
    return [_booking_to_response(b) for b in bookings]


# Admin assigns a booking to a provider
@router.post("/admin/{booking_id}/assign")
def admin_assign_booking(
    booking_id: int,
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    provider = db.query(User).filter(User.id == provider_id, User.role == "provider").first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
        
    booking.provider_id = provider_id
    booking.status = "pending"
    db.commit()
    db.refresh(booking)

    loaded = _load_booking_with_relations(db, booking.id)
    return _booking_to_response(loaded)
