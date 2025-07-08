from app.models.category import Category
from app.models.events import Event as EventModel
from app.schemas.events import Event, EventUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.events import EventCreate

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


@router.get("/", response_model=list[Event])
def get_events(
    db: Session = Depends(get_db),
):
    try:
        events = db.query(EventModel).all()
        return events
    except Exception as e:
        print(f"Error getting events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get events",
        )


@router.get("/{event_id}", response_model=Event)
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
