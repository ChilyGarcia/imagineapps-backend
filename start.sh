set -e

mkdir -p /app/data

echo "Aplicando migraciones con Alembic..."
alembic upgrade head

echo "Iniciando la aplicación..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
