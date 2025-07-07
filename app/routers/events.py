from app.models.category import Category
from app.models.events import Event as EventModel
from app.schemas.events import Event
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
def create_event(event_create: EventCreate,
                 current_user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    try:
        category_id = event_create.category_id
        category = db.query(Category).filter(
            Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found")

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create event")
