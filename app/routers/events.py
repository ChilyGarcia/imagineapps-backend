from app.models.category import Category
from app.models.events import Event as EventModel
from app.schemas.events import Event, EventResponse, EventCreate, EventUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(
    event_create: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        category_id = event_create.category_id
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )

        event_data = event_create.model_dump()
        event_data["user_id"] = current_user.id
        new_event = EventModel(**event_data)

        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        return new_event
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        print(f"Error creating event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event",
        )


class TimeFilter(str, Enum):
    today = "today"
    week = "week"
    month = "month"
    year = "year"


@router.get("/", response_model=list[EventResponse])
def get_events(
    category_id: Optional[int] = None,
    time_filter: Optional[TimeFilter] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db),
):

    try:
        query = db.query(EventModel)

        if category_id is not None:
            query = query.filter(EventModel.category_id == category_id)

        if date is not None:
            try:
                specific_date = datetime.strptime(date, "%Y-%m-%d").replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                next_day = specific_date + timedelta(days=1)
                query = query.filter(
                    EventModel.start_date >= specific_date,
                    EventModel.start_date < next_day,
                )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format. Use YYYY-MM-DD",
                )

        elif time_filter:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            if time_filter == TimeFilter.today:
                tomorrow = today + timedelta(days=1)
                query = query.filter(
                    EventModel.start_date >= today, EventModel.start_date < tomorrow
                )
            elif time_filter == TimeFilter.week:
                monday = today - timedelta(days=today.weekday())
                next_monday = monday + timedelta(days=7)
                query = query.filter(
                    EventModel.start_date >= monday, EventModel.start_date < next_monday
                )
            elif time_filter == TimeFilter.month:
                start_of_month = today.replace(day=1)
                if today.month == 12:
                    start_of_next_month = today.replace(
                        year=today.year + 1, month=1, day=1
                    )
                else:
                    start_of_next_month = today.replace(month=today.month + 1, day=1)
                query = query.filter(
                    EventModel.start_date >= start_of_month,
                    EventModel.start_date < start_of_next_month,
                )
            elif time_filter == TimeFilter.year:
                start_of_year = today.replace(month=1, day=1)
                start_of_next_year = today.replace(year=today.year + 1, month=1, day=1)
                query = query.filter(
                    EventModel.start_date >= start_of_year,
                    EventModel.start_date < start_of_next_year,
                )

        events = query.all()
        return events
    except Exception as e:
        print(f"Error getting events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get events",
        )


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    try:
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found",
            )
        return event
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get event",
        )


@router.put("/{event_id}", response_model=Event, summary="Update an event")
def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:
        event = (
            db.query(EventModel)
            .filter(
                EventModel.id == event_id,
                EventModel.user_id == current_user.id,
            )
            .first()
        )
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found",
            )

        update_data = event_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event, key, value)
        db.commit()
        db.refresh(event)
        return event
    except HTTPException:
        raise
    except Exception as e:
        import logging

        logging.error(f"Error updating event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update event",
        )


@router.delete("/{event_id}", summary="Delete an event")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        event = (
            db.query(EventModel)
            .filter(
                EventModel.id == event_id,
                EventModel.user_id == current_user.id,
            )
            .first()
        )
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found",
            )
        db.delete(event)
        db.commit()
        return {"message": "Event deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        import logging

        logging.error(f"Error deleting event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete event",
        )
