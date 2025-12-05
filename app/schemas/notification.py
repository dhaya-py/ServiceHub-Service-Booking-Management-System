from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    booking_id: Optional[int]
    channel: str
    type: str
    message: str
    is_sent: bool
    created_at: datetime
    sent_at: Optional[datetime]

    class Config:
        from_attributes = True
