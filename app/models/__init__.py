# Define los modelos que se exportan desde este paquete
__all__ = ['User', 'Category', 'Event']

# Importa todos los modelos para que SQLAlchemy los inicialice correctamente
from app.models.user import User
from app.models.category import Category
from app.models.events import Event
