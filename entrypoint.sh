#!/bin/sh

set -e

echo "Waiting for PostgreSQL"
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
    sleep 1
done

# проверяем что миграции принялись
echo "Checking for unapplied migrations ..."
python manage.py makemigrations --check --dry-run

# Создаем миграции
echo "Applyting migrations .."
python manage.py migrate --noinput

# Собираем статику
echo "Collecting static ..."
python manage.py collectstatic --noinput

# Запускаем проет
echo "Starting application"
exec "$@"