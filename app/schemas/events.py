from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    category_id: int
    user_id: int


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True
