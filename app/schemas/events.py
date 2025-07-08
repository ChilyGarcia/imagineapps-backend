from pydantic import BaseModel
from datetime import datetime
from typing import Optional


from app.schemas.user import User
from app.schemas.category import Category

class EventBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    category_id: int
    user_id: int
    start_time: Optional[datetime] = None
    prize: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    id: int
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    start_time: Optional[datetime] = None
    prize: Optional[str] = None
    category: Category
    user: User

    class Config:
        from_attributes = True
