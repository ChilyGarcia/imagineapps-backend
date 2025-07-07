import logging
from app.db.session import SessionLocal
from app.seeders.category_seeder import CategorySeeder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_all_seeders():
    logger.info("Starting database seeding process...")
    db = SessionLocal()

    try:
        logger.info("Running Category seeder...")
        categories = CategorySeeder.seed(db)
        logger.info(f"✓ Successfully seeded {len(categories)} categories")
        for category in categories:
            logger.info(f"  - {category.name}")

        logger.info("✓ All database seeders completed successfully!")

    except Exception as e:
        logger.error(f"✗ Error running seeders: {str(e)}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run_all_seeders()
