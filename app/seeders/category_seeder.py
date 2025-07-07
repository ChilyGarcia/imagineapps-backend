from typing import List
from sqlalchemy.orm import Session
from app.models.category import Category
from app.db.session import SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CategorySeeder:

    @staticmethod
    def get_predefined_categories() -> List[dict]:
        return [{
            "name":
            "Tecnología",
            "description":
            "Eventos relacionados con avances tecnológicos, informática, "
            "desarrollo de software, hardware y tendencias digitales."
        }, {
            "name":
            "Artes",
            "description":
            "Eventos culturales y artísticos que incluyen música, pintura, "
            "escultura, literatura, teatro y otras formas de expresión artística."
        }, {
            "name":
            "Política",
            "description":
            "Eventos relacionados con gobernanza, políticas públicas, "
            "elecciones y asuntos gubernamentales."
        }]

    @staticmethod
    def seed(db_session: Session = None) -> List[Category]:
        session_created = False
        if db_session is None:
            db_session = SessionLocal()
            session_created = True

        created_categories = []

        try:
            existing_count = db_session.query(Category).count()
            if existing_count > 0:
                logger.info(
                    f"Categories already seeded. Found {existing_count} existing categories."
                )
                return db_session.query(Category).all()

            categories_data = CategorySeeder.get_predefined_categories()
            for category_data in categories_data:
                category = Category(**category_data)
                db_session.add(category)
                created_categories.append(category)

            db_session.commit()
            logger.info(
                f"Successfully seeded {len(created_categories)} categories.")

            return created_categories

        except Exception as e:
            db_session.rollback()
            logger.error(f"Error seeding categories: {str(e)}")
            raise

        finally:
            if session_created:
                db_session.close()


def run_seeder():
    try:
        categories = CategorySeeder.seed()
        print(f"✓ Successfully seeded {len(categories)} categories")
        for category in categories:
            print(f"  - {category.name}")
    except Exception as e:
        print(f"✗ Failed to seed categories: {str(e)}")


if __name__ == "__main__":
    run_seeder()
