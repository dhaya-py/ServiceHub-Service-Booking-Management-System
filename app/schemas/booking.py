from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional

# --- CREATE ---
class BookingCreate(BaseModel):
    service_id: int
    provider_id: int
    booking_date: date
    booking_time: time
    address: str
    amount: float


# --- UPDATE (Provider or Admin) ---
class BookingUpdate(BaseModel):
    status: Optional[str] = Field(
        default=None,
        description="Allowed values: pending, accepted, rejected, completed, canceled"
    )


# --- RESPONSE ---
class BookingResponse(BaseModel):
    id: int
    customer_id: int
    provider_id: int
    service_id: int
    booking_date: date
    booking_time: time
    address: str
    amount: float
    status: str
    payment_status: Optional[str] = "pending"
    created_at: datetime
    updated_at: Optional[datetime]

    # Computed fields from relationships
    service_name: Optional[str] = None
    provider_name: Optional[str] = None
    provider_email: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_names(cls, booking):
        data = {
            "id": booking.id,
            "customer_id": booking.customer_id,
            "provider_id": booking.provider_id,
            "service_id": booking.service_id,
            "booking_date": booking.booking_date,
            "booking_time": booking.booking_time,
            "address": booking.address,
            "amount": booking.amount,
            "status": booking.status,
            "payment_status": getattr(booking, "payment_status", "pending"),
            "created_at": booking.created_at,
            "updated_at": booking.updated_at,
            "service_name": booking.service.name if booking.service else None,
            "provider_name": booking.provider.name if booking.provider else None,
            "provider_email": booking.provider.email if booking.provider else None,
            "customer_name": booking.customer.name if booking.customer else None,
            "customer_email": booking.customer.email if booking.customer else None,
        }
        return cls(**data)
