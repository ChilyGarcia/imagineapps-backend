from fastapi import APIRouter, Depends, HTTPException, status
from app.models.category import Category as CategoryModel
from app.schemas.category import Category
from app.dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[Category])
def get_categories(
    db: Session = Depends(get_db),
):
    try:
        categories = db.query(CategoryModel).all()
        return categories
    except Exception as e:
        print(f"Error getting categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get categories",
        )
