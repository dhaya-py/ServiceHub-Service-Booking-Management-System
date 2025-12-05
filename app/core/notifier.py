from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models.notification import Notification
from app.core.email import send_email

def dispatch_notification(db: Session, *, user, booking, type: str, message: str):
    record = Notification(
        user_id=user.id,
        booking_id=booking.id if booking else None,
        channel="email",  # for now only email
        type=type,
        message=message,
        is_sent=False,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # Try sending email now (sync)
    success = send_email(
        to_email=user.email,
        subject=f"Booking Update: {type}",
        body=message,
    )

    if success:
        record.is_sent = True
        record.sent_at = datetime.utcnow()
        db.commit()

    return record
