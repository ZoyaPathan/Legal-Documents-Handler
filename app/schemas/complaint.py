from datetime import datetime
from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: str
    urgency: str
    preferred_lawyer_id: int | None = None


class ComplaintOut(BaseModel):
    id: int
    client_id: int
    preferred_lawyer_id: int | None = None

    title: str
    description: str
    category: str
    urgency: str

    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True