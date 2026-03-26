from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="completed")
    transaction_id = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    booking = relationship("Booking", foreign_keys=[booking_id])
    customer = relationship("User", foreign_keys=[customer_id])
    provider = relationship("User", foreign_keys=[provider_id])
